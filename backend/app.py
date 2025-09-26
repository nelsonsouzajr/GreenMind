from flask import Flask, request, jsonify
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import base64

# --- 1. SETUP INICIAL ---
app = Flask(__name__)

# --- 2. CARREGAR O MODELO DE IA ---
MODEL_PATH = 'greenmind_model_efficientnet.h5'
print(f"Carregando o modelo de IA de: {MODEL_PATH}")
# Carregamos o modelo, compilá-lo não é necessário para inferência
model = tf.keras.models.load_model(MODEL_PATH, compile=False)
class_names = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']
print("Modelo carregado com sucesso.")

# --- 3. FUNÇÃO AUXILIAR CORRIGIDA ---
def prepare_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)
    
    # CORREÇÃO AQUI: Usar a função de pré-processamento oficial do EfficientNet
    processed_image = tf.keras.applications.efficientnet.preprocess_input(image_array)
    return processed_image

# --- 4. ROTAS DA API ---
@app.route("/")
def home():
    return "Servidor do GreenMind está no ar. Modelo de IA carregado."

@app.route("/predict", methods=['POST'])
def predict():
    if 'image' not in request.json:
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400

    try:
        image_data = base64.b64decode(request.json['image'])
        prepared_image = prepare_image(image_data)
        
        prediction = model.predict(prepared_image)[0]
        
        top_3_indices = np.argsort(prediction)[-3:][::-1]
        
        results = []
        for i in top_3_indices:
            result = {
                "prediction": class_names[i].replace('___', ' - ').replace('_', ' '),
                "confidence": f"{prediction[i]:.2%}"
            }
            results.append(result)

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': f'Erro ao processar a imagem: {str(e)}'}), 500

# --- 5. INICIAR O SERVIDOR ---
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')