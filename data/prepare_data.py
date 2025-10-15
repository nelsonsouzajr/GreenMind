import os, random, shutil

DATASET_PATH = "G:/Cursos/UNIVESP/2025-2/Projeto Integrador/GreenMind/data/all_images/"
TRAIN_PATH = "G:/Cursos/UNIVESP/2025-2/Projeto Integrador/GreenMind/data/data_species/greenmind_final_dataset/train"
VAL_PATH = "G:/Cursos/UNIVESP/2025-2/Projeto Integrador/GreenMind/data/data_species/greenmind_final_dataset/val"
TEST_PATH = "G:/Cursos/UNIVESP/2025-2/Projeto Integrador/GreenMind/data/data_species/greenmind_final_dataset/test"

for class_id in os.listdir(DATASET_PATH):
    class_src = os.path.join(DATASET_PATH, class_id)
    images = [f for f in os.listdir(class_src) if os.path.isfile(os.path.join(class_src, f))]
    random.shuffle(images)
    n_total = len(images)
    n_val = max(1, int(0.1 * n_total))
    n_test = max(1, int(0.1 * n_total))
    n_train = n_total - n_val - n_test

    # Criar pastas de destino
    for folder in [TRAIN_PATH, VAL_PATH, TEST_PATH]:
        os.makedirs(os.path.join(folder, class_id), exist_ok=True)

    # Mover arquivos
    for i, img in enumerate(images):
        src_path = os.path.join(class_src, img)
        if i < n_train:
            dst_path = os.path.join(TRAIN_PATH, class_id, img)
        elif i < n_train + n_val:
            dst_path = os.path.join(VAL_PATH, class_id, img)
        else:
            dst_path = os.path.join(TEST_PATH, class_id, img)
        shutil.copy2(src_path, dst_path)
