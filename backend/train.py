import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# =====================
# CONFIGURAÇÕES
# =====================
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 50
LR = 1e-4  # começa maior, depois callbacks reduzem se necessário

DATA_DIR = "G:/Cursos/UNIVESP/2025-2/Projeto Integrador/GreenMind/data/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)"  # ajuste para sua pasta (subpastas = classes)

# =====================
# DATASET
# =====================
train_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

# Captura class_names ANTES do prefetch
class_names = train_ds.class_names
print("Classes detectadas:", class_names)

# Prefetch para performance
train_ds = train_ds.prefetch(buffer_size=tf.data.AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=tf.data.AUTOTUNE)

# =====================
# AUGMENTAÇÃO
# =====================
data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
    layers.RandomContrast(0.2),
    layers.RandomTranslation(0.1, 0.1),
    layers.Lambda(lambda x: x + tf.random.uniform(tf.shape(x), -0.2, 0.2))  # simula brilho
])

# =====================
# BALANCEAMENTO DE CLASSES
# =====================
counts = {name: 0 for name in class_names}
for _, labels in train_ds.unbatch():
    for l in labels.numpy():
        counts[class_names[l]] += 1

total = sum(counts.values())
class_weight = {
    i: total / (len(class_names) * counts[cname])
    for i, cname in enumerate(class_names)
}
print("Class Weights:", class_weight)

# =====================
# MODELO
# =====================
base_model = keras.applications.EfficientNetB0(
    input_shape=IMG_SIZE + (3,),
    include_top=False,
    weights="imagenet"
)
base_model.trainable = False  # congela no início

inputs = keras.Input(shape=IMG_SIZE + (3,))
x = data_augmentation(inputs)
x = keras.applications.efficientnet.preprocess_input(x)
x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(len(class_names), activation="softmax")(x)

model = keras.Model(inputs, outputs)

# Compilação
optimizer = keras.optimizers.Adam(learning_rate=LR)
model.compile(
    optimizer=optimizer,
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# =====================
# CALLBACKS
# =====================
callbacks = [
    keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=3,
        min_lr=1e-6
    )
]

# =====================
# TREINAMENTO (congelado)
# =====================
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    class_weight=class_weight,
    callbacks=callbacks
)

# =====================
# FINE-TUNING
# =====================
base_model.trainable = True
for layer in base_model.layers[:-20]:  # libera só últimas camadas
    layer.trainable = False

model.compile(
    optimizer=keras.optimizers.Adam(1e-5),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history_fine = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    class_weight=class_weight,
    callbacks=callbacks
)

# =====================
# SALVAR MODELO
# =====================
model.save("efficientnet_model.h5")
print("Modelo salvo em efficientnet_model.h5")
