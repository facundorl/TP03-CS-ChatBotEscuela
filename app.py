from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import numpy as np
import pickle
import unicodedata
import tensorflow as tf


app = Flask(__name__)
app.json.ensure_ascii = False  
CORS(app)  

def normalize_text(text):
    """Normaliza texto: pasa a minúsculas y quita acentos/tildes para tolerar faltas de ortografía (RF-01)."""
    text = text.lower()
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

# Cargar el modelo de IA entrenado y las estructuras de datos
model = tf.keras.models.load_model('chatbot_model.h5')
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

with open('intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)


INTENTS_BY_TAG = {i['tag']: i for i in intents['intents']}


SUGERENCIAS_FALLBACK = ['especialidades', 'inscripciones', 'contacto_ubicacion']


def build_sugerencias(tag):
    """Devuelve los temas relacionados a un intent, listos para mostrar como botones.

    Cada sugerencia incluye:
      - tag: identificador del intent relacionado
      - titulo: texto visible en el botón
      - consulta: frase que el frontend reenvía al hacer clic (un pattern real,
        para garantizar que la red neuronal lo reconozca)
    """
    if tag is None:
        tags_relacionados = SUGERENCIAS_FALLBACK
    else:
        intent = INTENTS_BY_TAG.get(tag)
        if not intent:
            return []
        tags_relacionados = intent.get('sugerencias', [])

    sugerencias = []
    for rel_tag in tags_relacionados:
        rel = INTENTS_BY_TAG.get(rel_tag)
        if not rel:
            continue
        sugerencias.append({
            'tag': rel_tag,
            'titulo': rel.get('titulo', rel_tag.replace('_', ' ').capitalize()),
            'consulta': rel['patterns'][0]
        })
    return sugerencias

# Función auxiliar para convertir la oración en palabras limpias
def clean_up_sentence(sentence):
    norm = normalize_text(sentence)
    clean_words = [w.strip('?!¡.,:;()"-') for w in norm.split()]
    return [w for w in clean_words if len(w) > 0]

# Función para armar la bolsa de palabras (Bag of Words)
def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)


STOPWORDS = {'de', 'la', 'el', 'en', 'para', 'con', 'por', 'un', 'una', 'los', 'las', 'y', 'o', 'al', 'del', 'se', 'lo', 'su', 'mi', 'tu', 'es', 'son', 'que'}


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "online",
        "mensaje": "Servidor Chatbot ET 36 D.E. 15 activo",
        "endpoint_chat": "/chat (método POST)"
    })

# RUTA DE RED PRINCIPAL 
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"response": "Formato de datos no válido. Se espera un JSON con 'message'."}), 400

    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"response": "No enviaste ningún mensaje. Por favor, escribí tu consulta."}), 400

    sentence_words = clean_up_sentence(user_message)

    recognized_meaningful = [w for w in sentence_words if w in words and w not in STOPWORDS]

    fallback_msg = (
        "Disculpá, no logré comprender tu consulta sobre ese trámite escolar. "
        "Por favor, comunicate con Secretaría o Preceptoría al correo info@et36.com.ar, "
        "det_36_de15@bue.edu.ar o acercate a la escuela en Galván 3700 (Polo Saavedra)."
    )

    if not recognized_meaningful:
        return jsonify({
            "response": fallback_msg,
            "intent": None,
            "confidence": 0.0,
            "sugerencias": build_sugerencias(None)
        })


    p = bow(user_message, words)
    res = model.predict(np.array([p]), verbose=0)[0]


    ERROR_THRESHOLD = 0.60
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)


    response_text = ""
    intent_tag = None
    confidence = 0.0

    if results:
        intent_tag = classes[results[0][0]]
        confidence = float(results[0][1])
        for i in intents['intents']:
            if i['tag'] == intent_tag:
                response_text = i['responses'][0]
                break
    else:
        response_text = fallback_msg

    return jsonify({
        "response": response_text,
        "intent": intent_tag,
        "confidence": round(confidence, 4),
        "sugerencias": build_sugerencias(intent_tag)
    })

if __name__ == '__main__':
    print("Iniciando servidor Flask en http://localhost:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
