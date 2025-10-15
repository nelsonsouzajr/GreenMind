import os
import json
import shutil
import splitfolders
import sys

# --- 1. CONFIGURAÇÃO ---
BASE_DATA_PATH = "G:/Cursos/UNIVESP/2025-2/Projeto Integrador/GreenMind/data/data_species"
RAW_CUSTOM_PATH = os.path.join(BASE_DATA_PATH, 'raw_species_dataset')
PLANTNET_PATH = os.path.join(BASE_DATA_PATH, 'plantnet_300K')
PLANTNET_TRAIN_IMAGES_PATH = os.path.join(PLANTNET_PATH, 'test', 'train', 'val' ) # Caminho para as imagens de treino do Pl@ntNet
JSON_ID_TO_NAME_PATH = os.path.join(PLANTNET_PATH, 'plantnet300K_species_id_2_name.json')

# Pastas de saída
UNIFIED_STAGING_PATH = os.path.join(BASE_DATA_PATH, 'unified_staging') # Onde tudo será unificado com IDs numéricos
FINAL_DATA_PATH = os.path.join(BASE_DATA_PATH, 'greenmind_final_dataset') # Onde o dataset final dividido será salvo
FINAL_JSON_MAP_PATH = "greenmind_species_id_2_name.json"
FINAL_CLASS_LIST_PATH = "class_names.txt"


def prepare_final_dataset():
    print("--- A iniciar a preparação final do dataset ---")
    os.makedirs(UNIFIED_STAGING_PATH, exist_ok=True)

    # --- Passo 1: Carregar o mapa do Pl@ntNet ---
    try:
        with open(JSON_ID_TO_NAME_PATH, 'r', encoding='utf-8') as f:
            id_to_name_map = json.load(f)
        name_to_id_map = {v.lower().strip(): k for k, v in id_to_name_map.items()}
        highest_id = max([int(k) for k in id_to_name_map.keys()])
        print(f"Mapa Pl@ntNet carregado com {len(id_to_name_map)} espécies.")
    except FileNotFoundError:
        print(f"ERRO: Ficheiro JSON do Pl@ntNet não encontrado em '{JSON_ID_TO_NAME_PATH}'.")
        return

    # --- Passo 2: Copiar as imagens do Pl@ntNet para a pasta de staging ---
    print("\nA copiar imagens do Pl@ntNet para a pasta de staging...")
    if os.path.exists(PLANTNET_TRAIN_IMAGES_PATH):
        for id_folder in os.listdir(PLANTNET_TRAIN_IMAGES_PATH):
            shutil.copytree(os.path.join(PLANTNET_TRAIN_IMAGES_PATH, id_folder), 
                            os.path.join(UNIFIED_STAGING_PATH, id_folder), 
                            dirs_exist_ok=True)
        print("Imagens do Pl@ntNet copiadas.")
    else:
        print(f"AVISO: Pasta de imagens do Pl@ntNet não encontrada em '{PLANTNET_TRAIN_IMAGES_PATH}'.")

    # --- Passo 3: Processar e unificar os seus datasets customizados ---
    print(f"\nA processar os seus datasets customizados de '{RAW_CUSTOM_PATH}'...")
    if not os.path.exists(RAW_CUSTOM_PATH):
        print(f"AVISO: A pasta '{RAW_CUSTOM_PATH}' não foi encontrada. A pular esta etapa.")
    else:
        for species_folder_name in os.listdir(RAW_CUSTOM_PATH):
            species_path = os.path.join(RAW_CUSTOM_PATH, species_folder_name)
            if not os.path.isdir(species_path): continue

            species_name_lower = species_folder_name.lower().replace('_', ' ').strip()
            target_id = None

            if species_name_lower in name_to_id_map:
                target_id = name_to_id_map[species_name_lower]
                print(f"  - '{species_folder_name}' corresponde ao ID Pl@ntNet: {target_id}")
            else:
                highest_id += 1
                target_id = str(highest_id)
                id_to_name_map[target_id] = species_folder_name # Adiciona a nova espécie ao mapa
                print(f"  - '{species_folder_name}' é uma nova espécie. Novo ID atribuído: {target_id}")

            # Copia as imagens para a pasta de staging com o ID numérico
            target_path = os.path.join(UNIFIED_STAGING_PATH, target_id)
            os.makedirs(target_path, exist_ok=True)
            for file_name in os.listdir(species_path):
                shutil.copy(os.path.join(species_path, file_name), os.path.join(target_path, file_name))

    # --- Passo 4: Guardar o mapa JSON unificado ---
    with open(FINAL_JSON_MAP_PATH, 'w', encoding='utf-8') as f:
        json.dump(id_to_name_map, f, indent=4, ensure_ascii=False)
    print(f"\nMapa unificado com {len(id_to_name_map)} espécies salvo em '{FINAL_JSON_MAP_PATH}'.")

    # --- Passo 5: Dividir o dataset unificado ---
    print("\nA dividir o dataset unificado em treino, validação e teste (80/10/10)...")
    if not os.path.exists(os.path.join(FINAL_DATA_PATH, 'train')):
        splitfolders.ratio(UNIFIED_STAGING_PATH, output=FINAL_DATA_PATH, seed=1337, ratio=(.8, .1, .1))
        print("Divisão concluída.")
    else:
        print("Dados já divididos.")

    # --- Passo 6: Gerar a lista final de classes ---
    print("\nA gerar a lista final de classes...")
    try:
        final_classes_ids = sorted(os.listdir(os.path.join(FINAL_DATA_PATH, 'train')))
        final_classes_names = [id_to_name_map.get(id, f"ID_DESCONHECIDO_{id}") for id in final_classes_ids]
        with open(FINAL_CLASS_LIST_PATH, 'w', encoding='utf-8') as f:
            for name in final_classes_names:
                f.write(f"{name}\n")
        print(f"Lista de {len(final_classes_names)} classes salva com sucesso em '{FINAL_CLASS_LIST_PATH}'!")
    except Exception as e:
        print(f"ERRO ao gerar lista de classes: {e}")

if __name__ == "__main__":
    prepare_final_dataset()