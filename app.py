import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Pega a chave das configurações do Render
API_KEY = os.environ.get("GOOGLE_API_KEY")

@app.route('/')
def home():
    return "Robô VIVO! (Modo Direto)"

@app.route('/chat', methods=['POST'])
def chat():
    dados = request.json
    pergunta = dados.get('mensagem')
    
    if not pergunta:
        return jsonify({"erro": "Escreva alguma coisa!"}), 400

    if not API_KEY:
        return jsonify({"erro": "Chave de API não configurada no Render"}), 500

    # AQUI ESTÁ O SEGREDO:
    # Vamos chamar o link direto do Google, sem usar a biblioteca problemática.
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": pergunta}]
        }]
    }

    try:
        # Envia o pedido
        response = requests.post(url, headers=headers, json=payload)
        resultado = response.json()
        
        # Se o Google retornar erro, mostra o erro real
        if "error" in resultado:
            mensagem_erro = resultado["error"].get("message", "Erro desconhecido do Google")
            return jsonify({"erro": f"Google recusou: {mensagem_erro}"}), 500
            
        # Se deu certo, extrai a resposta
        try:
            texto_resposta = resultado["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"resposta": texto_resposta})
        except:
            return jsonify({"erro": "O Google respondeu, mas o formato estava estranho."}), 500
        
    except Exception as e:
        return jsonify({"erro": f"Erro de conexão: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
