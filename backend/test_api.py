import requests
import base64
import json

# --- CONFIGURAÇÃO ---
# 1. Altere este caminho para uma imagem de folha de planta no seu computador
IMAGE_PATH = 'G:/Cursos/UNIVESP/2025-2/Projeto Integrador/GreenMind/data/test/AppleCedarRust2.jpg' 

# 2. O endereço do nosso servidor local
API_URL = 'http://127.0.0.1:5000/predict'

# --- SCRIPT DE TESTE ---
try:
    # Abrir a imagem em modo de leitura binária
    with open(IMAGE_PATH, 'rb') as image_file:
        # Codificar a imagem em base64
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    # Preparar o payload JSON
    payload = {'image': encoded_string}

    # Definir os headers
    headers = {'Content-Type': 'application/json'}

    # Enviar a requisição POST
    print(f"Enviando imagem para {API_URL}...")
    response = requests.post(API_URL, json=payload, headers=headers)

    # Imprimir o resultado
    print("\n--- Resposta do Servidor ---")
    print(f"Status Code: {response.status_code}")
    print("JSON Recebido:", response.json())
    print("--------------------------")

except FileNotFoundError:
    print(f"ERRO: Arquivo de imagem não encontrado em '{IMAGE_PATH}'. Por favor, verifique o caminho.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")