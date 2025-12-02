import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GOOGLE_API_KEY")

@app.route('/')
def home():
    return "Robô VIVO! (Gemini 1.5 Flash)"

@app.route('/chat', methods=['POST'])
def chat():
    dados = request.json
    pergunta = dados.get('mensagem')
    
    if not pergunta:
        return jsonify({"erro": "Escreva alguma coisa!"}), 400

    if not API_KEY:
        return jsonify({"erro": "Chave de API não configurada"}), 500

    # URL CORRETA PARA O MODELO FLASH (V1BETA)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": pergunta}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        resultado = response.json()
        
        if "error" in resultado:
            msg = resultado["error"].get("message", "Erro desconhecido")
            return jsonify({"erro": f"Google recusou: {msg}"}), 500
            
        try:
            texto = resultado["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"resposta": texto})
        except:
            return jsonify({"erro": "Resposta estranha do Google."}), 500
        
    except Exception as e:
        return jsonify({"erro": f"Erro de conexão: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
