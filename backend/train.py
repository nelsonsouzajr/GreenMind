import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import os
import numpy as np
from sklearn.utils import class_weight

# --- 1. CONFIGURAÇÃO ---
DATASET_PATH = "G:/Cursos/UNIVESP/2025-2/Projeto Integrador/GreenMind/data/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
INITIAL_EPOCHS = 50
FINE_TUNE_EPOCHS = 30
TOTAL_EPOCHS = INITIAL_EPOCHS + FINE_TUNE_EPOCHS

# --- 2. PREPARAÇÃO DOS DADOS ---
print("Carregando e preparando os dados...")
train_dir = os.path.join(DATASET_PATH, 'train')
validation_dir = os.path.join(DATASET_PATH, 'valid')

# Carrega os datasets sem pré-processamento para pegar os rótulos
temp_train_dataset = tf.keras.utils.image_dataset_from_directory(train_dir, shuffle=False)
class_names = temp_train_dataset.class_names
print(f"Encontradas {len(class_names)} classes.")

# Captura correta de class_names antes do prefetch
train_labels = np.concatenate([y for x, y in temp_train_dataset], axis=0)
#train_labels = np.argmax(train_labels, axis=1)

# Balanceamento de classes com class_weight
class_weights = class_weight.compute_class_weight('balanced', classes=np.unique(train_labels), y=train_labels)
class_weight_dict = dict(enumerate(class_weights))
print("Pesos de classe calculados para balanceamento.")

# Agora, cria os datasets para o treinamento de fato
train_dataset = tf.keras.utils.image_dataset_from_directory(
    train_dir, label_mode='categorical', shuffle=True, image_size=IMG_SIZE, batch_size=BATCH_SIZE
)
validation_dataset = tf.keras.utils.image_dataset_from_directory(
    validation_dir, label_mode='categorical', shuffle=False, image_size=IMG_SIZE, batch_size=BATCH_SIZE
)
AUTOTUNE = tf.data.AUTOTUNE
train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)

# --- 3. CONSTRUÇÃO DO MODELO AVANÇADO ---
print("Construindo o modelo com EfficientNetB0...")
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip('horizontal'),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.2),
    layers.RandomTranslation(height_factor=0.1, width_factor=0.1),
    layers.RandomContrast(0.2)
], name="data_augmentation")

IMG_SHAPE = IMG_SIZE + (3,)
base_model = tf.keras.applications.EfficientNetB0(
    input_shape=IMG_SHAPE, include_top=False, weights='imagenet'
)
base_model.trainable = False

inputs = tf.keras.Input(shape=IMG_SHAPE)
x = data_augmentation(inputs)
x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.BatchNormalization()(x) # Adiciona BatchNormalization
x = layers.Dropout(0.5)(x) # Adiciona Dropout
outputs = layers.Dense(len(class_names), activation='softmax')(x)
model = tf.keras.Model(inputs, outputs)

# --- 4. COMPILAÇÃO E TREINAMENTO INICIAL ---
print("Compilando o modelo para treinamento inicial...")
model.compile(
    optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']
)
print(f"\nIniciando o treinamento inicial por {INITIAL_EPOCHS} épocas...")
history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=INITIAL_EPOCHS,
    class_weight=class_weight_dict # Usa os pesos de classe
)
print("Treinamento inicial concluído!")

# --- 5. PREPARAÇÃO E TREINAMENTO DE FINE-TUNING ---
base_model.trainable = True
fine_tune_at = -20 # Descongela as últimas 20 camadas do EfficientNet
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

# Callbacks para o treinamento inteligente
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.000001)

print("\nRecompilando o modelo para Fine-Tuning...")
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
print(f"\nIniciando o Fine-Tuning por mais {FINE_TUNE_EPOCHS} épocas...")
history_fine_tune = model.fit(
    train_dataset,
    epochs=TOTAL_EPOCHS,
    initial_epoch=history.epoch[-1],
    validation_data=validation_dataset,
    class_weight=class_weight_dict, # Usa os pesos de classe também no fine-tuning
    callbacks=[early_stopping, reduce_lr] # Adiciona os callbacks
)
print("Fine-Tuning concluído!")

# --- 6. VISUALIZAÇÃO DOS RESULTADOS ---
print("\nGerando gráficos de performance combinados...")
# Combina o histórico dos dois treinamentos
acc = history.history['accuracy'] + history_fine_tune.history['accuracy']
val_acc = history.history['val_accuracy'] + history_fine_tune.history['val_accuracy']
loss = history.history['loss'] + history_fine_tune.history['loss']
val_loss = history.history['val_loss'] + history_fine_tune.history['val_loss']

# Plota os gráficos
plt.figure(figsize=(15, 5))

plt.subplot(1, 2, 1)
plt.plot(acc, label='Acurácia de Treinamento')
plt.plot(val_acc, label='Acurácia de Validação')
plt.axvline(INITIAL_EPOCHS - 1, color='gray', linestyle='--', label='Início do Fine-Tuning')
plt.ylim([min(plt.ylim()), 1])
plt.legend(loc='lower right')
plt.title('Acurácia de Treinamento e Validação')
plt.xlabel('Épocas')
plt.ylabel('Acurácia')

plt.subplot(1, 2, 2)
plt.plot(loss, label='Perda de Treinamento')
plt.plot(val_loss, label='Perda de Validação')
plt.axvline(INITIAL_EPOCHS - 1, color='gray', linestyle='--', label='Início do Fine-Tuning')
plt.legend(loc='upper right')
plt.title('Perda de Treinamento e Validação')
plt.xlabel('Épocas')
plt.ylabel('Perda')

# Salva a figura ANTES de mostrar
plt.savefig('grafico_performance_final.png')
plt.show()

# --- 7. SALVAR O MODELO FINAL ---
print("\nSalvando o modelo final (pós Fine-Tuning)...")
# Note que o modelo salvo é o que foi treinado por último (com fine-tuning)
model.save('greenmind_model_efficientnet.h5')
print("Modelo final salvo com sucesso!")