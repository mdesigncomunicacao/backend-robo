import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# O CORS permite que o SEU site converse com esse servidor
CORS(app)

# Pega a chave dos "Segredos" do servidor (vamos configurar isso depois)
MINHA_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=MINHA_API_KEY)

# Configuração do modelo
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "O Robô está VIVO! Use a rota /chat para conversar."

@app.route('/chat', methods=['POST'])
def chat():
    dados = request.json
    pergunta = dados.get('mensagem')
    
    if not pergunta:
        return jsonify({"erro": "Escreva alguma coisa!"}), 400

    try:
        # Envia para o Gemini
        response = model.generate_content(pergunta)
        return jsonify({"resposta": response.text})
    except Exception as e:
        return jsonify({"erro": f"Erro no servidor: {str(e)}"}), 500

if __name__ == '__main__':
    # A porta deve ser pega do ambiente ou usar 10000 como padrão no Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
