#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.utils import class_weight
import matplotlib.pyplot as plt

# =====================================
# 1. CONFIGURAÇÃO
# =====================================
BASE_DATA_PATH = r"G:/Cursos/UNIVESP/2025-2/Projeto Integrador/GreenMind/data/data_species/greenmind_final_dataset/"
TRAIN_PATH = os.path.join(BASE_DATA_PATH, 'train')
VALID_PATH = os.path.join(BASE_DATA_PATH, 'val')
TEST_PATH = os.path.join(BASE_DATA_PATH, 'test')
JSON_MAP_PATH = "species_translation_map.json"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32 # SUA CORREÇÃO APLICADA! Começamos com 16 para poupar memória.
INITIAL_EPOCHS = 30
FINE_TUNE_EPOCHS = 20
TOTAL_EPOCHS = INITIAL_EPOCHS + FINE_TUNE_EPOCHS
AUTOTUNE = tf.data.AUTOTUNE

CHECKPOINT_DIR = "checkpoints"
os.makedirs(CHECKPOINT_DIR, exist_ok=True)
BEST_WEIGHTS_PATH = os.path.join(CHECKPOINT_DIR, "best_species_weights.h5")
LOG_CSV_PATH = os.path.join(CHECKPOINT_DIR, "species_training_log.csv")
FINAL_MODEL_PATH = "greenmind_model_species_final"

# =====================================
# 2. CONFIGURAÇÕES DE AMBIENTE
# =====================================
print("Versão do TensorFlow:", tf.__version__)
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
            tf.config.set_logical_device_configuration(
                gpu,
                [tf.config.LogicalDeviceConfiguration(memory_limit=3500)]  # Limite em MB, ajuste conforme sua GPU
            )
        print(f"GPUs disponíveis: {len(gpus)}. Memory growth habilitado e limite de memória configurado.")
        tf.keras.mixed_precision.set_global_policy('mixed_float16')
        print("Mixed precision (float16) ativado.")
    except RuntimeError as e:
        print("Aviso ao configurar GPU:", e)

# =====================================
# 3. CARREGAMENTO DOS DADOS
# =====================================
print("\n--- Fase de Carregamento dos Dados ---")
try:
    with open(JSON_MAP_PATH, 'r', encoding='utf-8') as f:
        species_map = json.load(f)
    print(f"Mapa de espécies carregado com {len(species_map)} entradas.")
except Exception as e:
    print(f"ERRO: Não foi possível carregar o mapa de espécies '{JSON_MAP_PATH}': {e}")
    sys.exit(1)

train_class_ids = sorted(os.listdir(TRAIN_PATH))
class_names = [species_map.get(id, {}).get("scientific_name", f"ID_DESCONHECIDO_{id}") for id in train_class_ids]
num_classes = len(class_names)
print(f"Encontradas {num_classes} classes de espécies.")

train_ds = tf.keras.utils.image_dataset_from_directory(
    TRAIN_PATH, label_mode='categorical', shuffle=True, image_size=IMG_SIZE, batch_size=BATCH_SIZE, class_names=train_class_ids
)
validation_ds = tf.keras.utils.image_dataset_from_directory(
    VALID_PATH, label_mode='categorical', shuffle=False, image_size=IMG_SIZE, batch_size=BATCH_SIZE, class_names=train_class_ids
)
test_ds = tf.keras.utils.image_dataset_from_directory(
    TEST_PATH, label_mode='categorical', shuffle=False, image_size=IMG_SIZE, batch_size=BATCH_SIZE, class_names=train_class_ids
)

# Calcular pesos de classe
print("A calcular pesos de classe...")
train_labels = np.concatenate([y for x, y in train_ds], axis=0)
train_labels_indices = np.argmax(train_labels, axis=1)
all_class_indices = np.arange(num_classes)
class_weights = class_weight.compute_class_weight('balanced', classes=all_class_indices, y=train_labels_indices)
class_weight_dict = dict(enumerate(class_weights))
print("Pesos de classe calculados com sucesso.")

# Otimização do pipeline
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
validation_ds = validation_ds.prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.prefetch(buffer_size=AUTOTUNE)

# =====================================
# 4. CONSTRUÇÃO DO MODELO
# =====================================
print("Construindo o modelo com EfficientNetB0...")
data_augmentation = keras.Sequential([
    layers.RandomFlip('horizontal'),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.2),
], name="data_augmentation")

base_model = tf.keras.applications.EfficientNetB0(input_shape=IMG_SIZE + (3,), include_top=False, weights='imagenet')
base_model.trainable = False

inputs = keras.Input(shape=IMG_SIZE + (3,))
x = data_augmentation(inputs)
x = tf.keras.applications.efficientnet.preprocess_input(x)
x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.5)(x)
outputs = layers.Dense(num_classes, activation='softmax', dtype='float32')(x)
model = keras.Model(inputs, outputs)

# =====================================
# 5. TREINO INICIAL
# =====================================
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
print(f"\nIniciando o treinamento inicial por {INITIAL_EPOCHS} épocas...")
history = model.fit(
    train_ds,
    epochs=INITIAL_EPOCHS,
    validation_data=validation_ds,
    class_weight=class_weight_dict
)

# =====================================
# 6. FINE-TUNING
# =====================================
base_model.trainable = True
fine_tune_at = -20
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

callbacks = [
    tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True, verbose=1),
    tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.000001, verbose=1),
    tf.keras.callbacks.ModelCheckpoint(filepath=BEST_WEIGHTS_PATH, save_weights_only=True, monitor='val_accuracy', mode='max', save_best_only=True, verbose=1),
    tf.keras.callbacks.CSVLogger(LOG_CSV_PATH)
]

print("\nRecompilando o modelo para Fine-Tuning...")
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print(f"\nIniciando o Fine-Tuning por mais {FINE_TUNE_EPOCHS} épocas...")
history_fine_tune = model.fit(
    train_ds,
    epochs=TOTAL_EPOCHS,
    initial_epoch=history.epoch[-1],
    validation_data=validation_ds,
    class_weight=class_weight_dict,
    callbacks=callbacks
)

# =====================================
# 7. AVALIAÇÃO E SALVAMENTO
# =====================================
print("\nCarregando os melhores pesos encontrados...")
model.load_weights(BEST_WEIGHTS_PATH)

print("\n--- Avaliação Final no Conjunto de Teste ---")
results = model.evaluate(test_ds)
print(f"Perda (Loss) no teste: {results[0]:.4f}")
print(f"Acurácia no teste: {results[1]:.2%}")

print("\nSalvando o modelo final...")
model.save(FINAL_MODEL_PATH + ".h5")
print(f"Modelo final salvo com sucesso em '{FINAL_MODEL_PATH}'")

# =====================================
# 8. VISUALIZAÇÃO
# =====================================
print("\nGerando gráficos de performance...")
acc = history.history['accuracy'] + history_fine_tune.history['accuracy']
val_acc = history.history['val_accuracy'] + history_fine_tune.history['val_accuracy']
loss = history.history['loss'] + history_fine_tune.history['loss']
val_loss = history.history['val_loss'] + history_fine_tune.history['val_loss']

plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
plt.plot(acc, label='Acurácia de Treinamento')
plt.plot(val_acc, label='Acurácia de Validação')
plt.axvline(INITIAL_EPOCHS - 1, color='gray', linestyle='--', label='Início do Fine-Tuning')
plt.legend(loc='lower right')
plt.title('Acurácia de Treinamento e Validação')

plt.subplot(1, 2, 2)
plt.plot(loss, label='Perda de Treinamento')
plt.plot(val_loss, label='Perda de Validação')
plt.axvline(INITIAL_EPOCHS - 1, color='gray', linestyle='--', label='Início do Fine-Tuning')
plt.legend(loc='upper right')
plt.title('Perda de Treinamento e Validação')

plt.savefig('grafico_performance_species_final.png')
plt.show()

print("\n--- Treino Concluído com Sucesso! ---")