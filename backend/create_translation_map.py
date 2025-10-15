import json
import os

## --- 1. CONFIGURAÇÃO ---
# Caminho para o ficheiro JSON original do Pl@ntNet
PLANTNET_JSON_PATH = "G:/Cursos/UNIVESP/2025-2/Projeto Integrador/GreenMind/data/data_species/plantnet_300K/plantnet300K_species_id_2_name.json"
# Caminho para o seu ficheiro JSON com as espécies customizadas
CUSTOM_JSON_PATH = "G:/Cursos/UNIVESP/2025-2/Projeto Integrador/GreenMind/data/data_species/greenmind_species_id_2_name.json" 
# Nome do novo ficheiro JSON unificado que vamos criar
OUTPUT_JSON_PATH = "species_translation_map.json"

# --- 2. SCRIPT DE GERAÇÃO DO MAPA UNIFICADO ---
def create_unified_map():
    # Carrega o mapa original do Pl@ntNet
    try:
        with open(PLANTNET_JSON_PATH, 'r', encoding='utf-8') as f:
            plantnet_map = json.load(f)
        print(f"Mapa Pl@ntNet carregado com {len(plantnet_map)} espécies.")
    except Exception as e:
        print(f"ERRO ao ler o ficheiro do Pl@ntNet: {e}")
        plantnet_map = {}

    # Carrega o seu mapa customizado
    try:
        with open(CUSTOM_JSON_PATH, 'r', encoding='utf-8') as f:
            custom_map = json.load(f)
        print(f"Seu mapa customizado foi carregado com {len(custom_map)} espécies.")
    except Exception as e:
        print(f"AVISO: Não foi possível ler o seu ficheiro de mapa customizado: {e}")
        custom_map = {}

    # Une os dois dicionários. Se houver chaves repetidas, as do seu mapa customizado terão prioridade.
    unified_map = {**plantnet_map, **custom_map}
    
    new_structured_map = {}
    
    print(f"\nA processar um total de {len(unified_map)} espécies...")
    for species_id, scientific_name in unified_map.items():
        new_structured_map[species_id] = {
            "scientific_name": scientific_name,
            "popular_name_en": "",
            "popular_name_pt": ""
        }

    with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(new_structured_map, f, indent=4, ensure_ascii=False)
        
    print(f"\nFicheiro '{OUTPUT_JSON_PATH}' unificado criado com sucesso!")

# --- EXECUÇÃO ---
if __name__ == "__main__":
    create_unified_map()