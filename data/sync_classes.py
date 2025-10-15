import os
import shutil

DATASET_PATH = r"G:/Cursos/UNIVESP/2025-2/Projeto Integrador/GreenMind/data/data_species/greenmind_final_dataset"
TRAIN_PATH = os.path.join(DATASET_PATH, "train")
VALID_PATH = os.path.join(DATASET_PATH, "val")
TEST_PATH  = os.path.join(DATASET_PATH, "test")

def get_classes(path):
    """Retorna um set com o nome das pastas de classes existentes."""
    return set([
        d for d in os.listdir(path)
        if os.path.isdir(os.path.join(path, d))
    ])

def remove_extra_folders(base_path, allowed_classes):
    """Remove pastas que não estão no conjunto de classes permitidas."""
    removed = 0
    for cls in os.listdir(base_path):
        full_path = os.path.join(base_path, cls)
        if os.path.isdir(full_path) and cls not in allowed_classes:
            shutil.rmtree(full_path)  # Apaga pasta e conteúdo
            removed += 1
    print(f"[{os.path.basename(base_path)}] {removed} pastas removidas.")

print("🔎 Verificando classes em cada diretório...")
train_classes = get_classes(TRAIN_PATH)
val_classes   = get_classes(VALID_PATH)
test_classes  = get_classes(TEST_PATH)

print(f"Train: {len(train_classes)} classes")
print(f"Val:   {len(val_classes)} classes")
print(f"Test:  {len(test_classes)} classes")

# Classes que estão em TODAS as pastas
common_classes = train_classes & val_classes & test_classes
print(f"✅ Classes em comum nas 3 pastas: {len(common_classes)}")

# Remover tudo que não estiver na interseção
remove_extra_folders(TRAIN_PATH, common_classes)
remove_extra_folders(VALID_PATH, common_classes)
remove_extra_folders(TEST_PATH,  common_classes)

print("🎯 Limpeza concluída!")
