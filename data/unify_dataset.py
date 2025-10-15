import os
import json
import shutil

# --- 1. CONFIGURAÇÃO ---
# Caminhos para os ficheiros e pastas (verifique se estão corretos)
BASE_DATA_PATH = "G:/Cursos/UNIVESP/2025-2/Projeto Integrador/GreenMind/data/data_species"
RAW_DATA_PATH = os.path.join(BASE_DATA_PATH, 'raw_species_dataset')
PLANTNET_PATH = os.path.join(BASE_DATA_PATH, 'plantnet_300K') # Corrigido para o nome exato da pasta
JSON_ID_TO_NAME_PATH = os.path.join(PLANTNET_PATH, 'plantnet300K_species_id_2_name.json')
CUSTOM_MAP_OUTPUT_PATH = "custom_species_map.json"

def unify_and_rename_datasets():
    print("--- A iniciar a unificação dos datasets ---")

    # --- Passo 1: Carregar o "dicionário" do Pl@ntNet ---
    try:
        with open(JSON_ID_TO_NAME_PATH, 'r', encoding='utf-8') as f:
            id_to_name_map = json.load(f)
        # Invertemos o dicionário para ter name -> id, para facilitar a busca
        name_to_id_map = {v.lower(): k for k, v in id_to_name_map.items()}
        # Encontramos o ID mais alto para sabermos onde começar a numerar as novas espécies
        highest_id = max([int(k) for k in id_to_name_map.keys()])
        print(f"Dicionário Pl@ntNet carregado. {len(name_to_id_map)} espécies encontradas.")
    except FileNotFoundError:
        print(f"ERRO: Ficheiro JSON do Pl@ntNet não encontrado em '{JSON_ID_TO_NAME_PATH}'.")
        return

    custom_species_map = {}
    next_new_id = highest_id + 1

    # --- Passo 2: Processar as suas pastas de espécies ---
    print(f"\nA processar as suas pastas em '{RAW_DATA_PATH}'...")
    if not os.path.exists(RAW_DATA_PATH):
        print(f"ERRO: A pasta '{RAW_DATA_PATH}' não foi encontrada.")
        return

    for species_folder_name in os.listdir(RAW_DATA_PATH):
        species_path = os.path.join(RAW_DATA_PATH, species_folder_name)
        if not os.path.isdir(species_path):
            continue # Ignora ficheiros, processa apenas pastas

        species_name_lower = species_folder_name.lower().replace('_', ' ')
        
        # Verifica se a espécie já existe no Pl@ntNet
        if species_name_lower in name_to_id_map:
            # Se sim, usa o ID existente do Pl@ntNet
            target_id = name_to_id_map[species_name_lower]
            print(f"  - '{species_folder_name}' já existe no Pl@ntNet. A unificar com ID: {target_id}")
            # Aqui, você faria a lógica de copiar as imagens para a pasta do Pl@ntNet
            # Ex: copy_images(species_path, os.path.join(PLANTNET_TRAIN_PATH, target_id))
        else:
            # Se não, atribui um novo ID
            target_id = str(next_new_id)
            print(f"  - '{species_folder_name}' é uma nova espécie. A atribuir novo ID: {target_id}")
            custom_species_map[target_id] = species_folder_name
            # Aqui, você renomearia a sua pasta para o novo ID
            # Ex: os.rename(species_path, os.path.join(RAW_DATA_PATH, target_id))
            next_new_id += 1
            
    # --- Passo 3: Salvar o mapa das novas espécies ---
    if custom_species_map:
        with open(CUSTOM_MAP_OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(custom_species_map, f, indent=4, ensure_ascii=False)
        print(f"\nMapa de {len(custom_species_map)} novas espécies salvo em '{CUSTOM_MAP_OUTPUT_PATH}'.")

    print("\n--- Processo de unificação concluído! ---")
    print("O próximo passo é unificar manualmente as pastas e depois executar o 'prepare_data.py'.")

# --- EXECUÇÃO ---
if __name__ == "__main__":
    # Esta é uma simulação. A lógica real de renomear/copiar precisará
    # ser implementada com base na sua organização final de pastas.
    unify_and_rename_datasets()