import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import os

# --- 1. CONFIGURAÇÃO ---
DATASET_PATH = "G:/Cursos/UNIVESP/2025-2/Projeto Integrador/GreenMind/data/greenmind_final_dataset/"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
INITIAL_EPOCHS = 250
FINE_TUNE_EPOCHS = 75 # Quantas épocas faremos o ajuste fino
TOTAL_EPOCHS = INITIAL_EPOCHS + FINE_TUNE_EPOCHS

# --- 2. PREPARAÇÃO DOS DADOS ---
print("Carregando e preparando os dados...")
train_dir = os.path.join(DATASET_PATH, 'train')
validation_dir = os.path.join(DATASET_PATH, 'valid')

train_dataset = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    label_mode='categorical',
    shuffle=True,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)
validation_dataset = tf.keras.utils.image_dataset_from_directory(
    validation_dir,
    label_mode='categorical',
    shuffle=False,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)
class_names = train_dataset.class_names
print(f"Encontradas {len(class_names)} classes.")
AUTOTUNE = tf.data.AUTOTUNE
train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)

# --- 3. CONSTRUÇÃO DO MODELO ---
print("Construindo o modelo...")
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip('horizontal'),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.2),
], name="data_augmentation")
IMG_SHAPE = IMG_SIZE + (3,)
base_model = tf.keras.applications.MobileNetV2(
    input_shape=IMG_SHAPE,
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False
inputs = tf.keras.Input(shape=IMG_SHAPE)
x = data_augmentation(inputs)
x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.5)(x) # <-- ADICIONE ESTA LINHA
outputs = layers.Dense(len(class_names), activation='softmax')(x)
model = tf.keras.Model(inputs, outputs)

# --- 4. COMPILAÇÃO E TREINAMENTO INICIAL ---
print("Compilando o modelo para treinamento inicial...")
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
print(f"\nIniciando o treinamento inicial por {INITIAL_EPOCHS} épocas...")
history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=INITIAL_EPOCHS
)
print("Treinamento inicial concluído!")

# --- 5. PREPARAÇÃO PARA O FINE-TUNING ---
base_model.trainable = True
fine_tune_at = 100
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False
print("\nRecompilando o modelo para Fine-Tuning...")
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
print("Modelo pronto para o Fine-Tuning.")

# --- 6. TREINAMENTO DE FINE-TUNING ---
print(f"\nIniciando o Fine-Tuning por mais {FINE_TUNE_EPOCHS} épocas...")
history_fine_tune = model.fit(
    train_dataset,
    epochs=TOTAL_EPOCHS,
    initial_epoch=history.epoch[-1],
    validation_data=validation_dataset
)
print("Fine-Tuning concluído!")

# --- 7. VISUALIZAÇÃO DOS RESULTADOS COMBINADOS ---
print("\nGerando gráficos de performance combinados...")
acc = history.history['accuracy'] + history_fine_tune.history['accuracy']
val_acc = history.history['val_accuracy'] + history_fine_tune.history['val_accuracy']
loss = history.history['loss'] + history_fine_tune.history['loss']
val_loss = history.history['val_loss'] + history_fine_tune.history['val_loss']

plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
plt.plot(acc, label='Acurácia de Treinamento')
plt.plot(val_acc, label='Acurácia de Validação')
plt.axvline(INITIAL_EPOCHS -1, color='gray', linestyle='--', label='Início do Fine-Tuning')
plt.ylim([min(plt.ylim()), 1])
plt.legend(loc='lower right')
plt.title('Acurácia de Treinamento e Validação')
plt.xlabel('Épocas')
plt.ylabel('Acurácia')

plt.subplot(1, 2, 2)
plt.plot(loss, label='Perda de Treinamento')
plt.plot(val_loss, label='Perda de Validação')
plt.axvline(INITIAL_EPOCHS -1, color='gray', linestyle='--', label='Início do Fine-Tuning')
plt.legend(loc='upper right')
plt.title('Perda de Treinamento e Validação')
plt.xlabel('Épocas')
plt.ylabel('Perda')
plt.show()

# --- 8. SALVAR O MODELO FINAL ---
print("\nSalvando o modelo final (pós Fine-Tuning)...")
model.save('greenmind_model_final.h5')
print("Modelo final salvo com sucesso!")