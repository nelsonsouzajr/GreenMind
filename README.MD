# GreenMind 🌱

## 📖 Sobre o Projeto (🇧🇷)

GreenMind é um aplicativo móvel desenvolvido como parte do Projeto Integrador da UNIVESP. O objetivo é criar uma ferramenta que utiliza Inteligência Artificial para ajudar horticultores, agricultores familiares e entusiastas da jardinagem a identificar espécies de plantas, diagnosticar problemas de saúde vegetal e receber sugestões de cuidados.

## 📖 About The Project (🇺🇸)

GreenMind is a mobile application developed as part of the UNIVESP Integrator Project. The goal is to create a tool that uses Artificial Intelligence to help horticulturists, family farmers, and gardening enthusiasts to identify plant species, diagnose plant health issues, and receive care suggestions.

---

## 📊 Status do Projeto (🇧🇷)

**Frontend:** Protótipo 100% funcional com o fluxo principal de telas implementado.
**Backend:** Primeiro modelo de Machine Learning (v1) treinado, atingindo uma acurácia de validação de ~71.5% após a técnica de Fine-Tuning. O modelo está salvo e pronto para ser integrado a uma API.

## 📊 Project Status (🇺🇸)

**Frontend:** A functional prototype with the main screen flow is 100% complete.
**Backend:** The first Machine Learning model (v1) has been trained, achieving a validation accuracy of ~71.5% after Fine-Tuning. The model is saved and ready to be served via an API.

---

## ✨ Funcionalidades (🇧🇷)

* **Frontend (React Native):**
    * Fluxo de 4 telas: Início, Captura, Análise (simulada) e Resultado (com dados de exemplo).
    * Seleção de imagem da câmera ou galeria do dispositivo.
    * Interface de usuário limpa e organizada.
* **Backend (Python & TensorFlow):**
    * Modelo de classificação de imagens treinado para 38 classes (espécies de plantas e doenças).
    * Arquitetura baseada em Transfer Learning com MobileNetV2.
    * Técnicas de Data Augmentation e Fine-Tuning para otimização da performance.

## ✨ Features (🇺🇸)

* **Frontend (React Native):**
    * A 4-screen flow: Home, Capture, Analysis (simulated), and Results (mock data).
    * Image selection from the device's camera or gallery.
    * A clean and organized user interface.
* **Backend (Python & TensorFlow):**
    * An image classification model trained on 38 classes (plant species and diseases).
    * Architecture based on Transfer Learning with MobileNetV2.
    * Data Augmentation and Fine-Tuning techniques for performance optimization.

---

## 🛠️ Tecnologias Utilizadas (🇧🇷)

* **Frontend:** React Native, Expo, Expo Router, TypeScript
* **Backend:** Python 3.9, TensorFlow 2.6, Keras 2.6, Matplotlib, NumPy

## 🛠️ Tech Stack (🇺🇸)

* **Frontend:** React Native, Expo, Expo Router, TypeScript
* **Backend:** Python 3.9, TensorFlow 2.6, Keras 2.6, Matplotlib, NumPy

---

## 💿 Dataset (🇧🇷)

Este projeto utiliza o "New Plant Diseases Dataset (Augmented)" disponível publicamente no Kaggle. Para executar o treinamento, é necessário baixar o dataset e extraí-lo para uma pasta `data/` na raiz do projeto.

* **Fonte:** [Kaggle - New Plant Diseases Dataset](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)

## 💿 Dataset (🇺🇸)

This project uses the "New Plant Diseases Dataset (Augmented)" publicly available on Kaggle. To run the training, you must download the dataset and extract it into a `data/` folder in the project root.

* **Source:** [Kaggle - New Plant Diseases Dataset](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)

---

## 🚀 Como Executar (🇧🇷)

### Frontend

1.  Navegue até a pasta do frontend: `cd frontend`
2.  Instale as dependências: `npm install`
3.  Inicie o projeto: `npx expo start`

### Backend

1.  Navegue até a pasta do backend: `cd backend`
2.  (Recomendado) Crie e ative um ambiente virtual.
3.  Instale as dependências (pode levar tempo): `pip install -r requirements.txt` (Nota: criar este arquivo é um próximo passo)
4.  Execute o script de treinamento: `python train.py`

## 🚀 Getting Started (🇺🇸)

### Frontend

1.  Navigate to the frontend folder: `cd frontend`
2.  Install dependencies: `npm install`
3.  Run the project: `npx expo start`

### Backend

1.  Navigate to the backend folder: `cd backend`
2.  (Recommended) Create and activate a virtual environment.
3.  Install dependencies (may take time): `pip install -r requirements.txt` (Note: creating this file is a next step)
4.  Run the training script: `python train.py`

---

## 🎨 Conceito da Logomarca (🇧🇷)

A logomarca é uma fusão minimalista e moderna entre o orgânico e o tecnológico. A silhueta principal é a de um cérebro humano, representando a inteligência e o aprendizado. No entanto, as circunvoluções e sulcos do cérebro são formados por linhas fluidas que se assemelham a galhos finos e entrelaçados. Pequenas folhas, com um design simples, brotam sutilmente de algumas dessas linhas. A paleta de cores é um gradiente de verdes, começando com um tom de verde musgo mais escuro na base (sugerindo conhecimento profundo) e clareando para um verde limão vibrante no topo (sugerindo novas ideias e saúde).

## 🎨 Logo Concept (🇺🇸)

The logo is a minimalist and modern fusion of the organic and the technological. The main silhouette is that of a human brain, representing intelligence and learning. However, the brain's gyri and sulci are formed by fluid lines resembling thin, intertwined branches. Small, simply designed leaves sprout subtly from some of these lines. The color palette is a gradient of greens, starting with a darker, mossy green at the base (suggesting deep knowledge) and brightening to a vibrant lime green at the top (suggesting new ideas and health).