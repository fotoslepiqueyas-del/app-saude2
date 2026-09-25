from flask import Flask, request, jsonify

# --- 1. Dados Manuais (Hardcoded) ---
hospitais_data = [
    {
        "id": 1,
        "nome": "Hospital Geral de Carapicuíba",
        "status": "Verde - Normal",
        "tempo_espera": 15
    },
    {
        "id": 2,
        "nome": "UPA Central Carapicuíba",
        "status": "Amarelo - Movimentado",
        "tempo_espera": 60
    },
    {
        "id": 3,
        "nome": "Hospital Santa Ana",
        "status": "Vermelho - Lotado",
        "tempo_espera": 180
    }
]

# Inicializa o aplicativo Flask
app = Flask(__name__)

# --- 2. Rotas Simples (Flask) ---

@app.route('/', methods=['GET'])
def home():
    return "API de Monitoramento de Hospitais em Carapicuíba. Acesse /hospitais para ver os dados."

@app.route('/hospitais', methods=['GET'])
def get_hospitais():
    return jsonify(hospitais_data)

@app.route('/hospitais/<int:hospital_id>', methods=['GET'])
def get_hospital(hospital_id):
    hospital = next((h for h in hospitais_data if h["id"] == hospital_id), None)
    if hospital:
        return jsonify(hospital)
    return jsonify({"message": "Hospital não encontrado"}), 404

@app.route('/hospitais/<int:hospital_id>', methods=['PUT'])
def update_hospital(hospital_id):
    hospital = next((h for h in hospitais_data if h["id"] == hospital_id), None)
    if not hospital:
        return jsonify({"message": "Hospital não encontrado"}), 404

    data = request.json
    if not data:
        return jsonify({"message": "Nenhum dado fornecido para atualização."}), 400

    updated = False
    if "status" in data:
        valid_statuses = ["Verde - Normal", "Amarelo - Movimentado", "Vermelho - Lotado"]
        if data["status"] not in valid_statuses:
            return jsonify({"message": f"Status inválido. Deve ser um de: {valid_statuses}"}), 400
        hospital["status"] = data["status"]
        updated = True

    if "tempo_espera" in data:
        try:
            wait_time = int(data["tempo_espera"])
            if wait_time < 0:
                raise ValueError
            hospital["tempo_espera"] = wait_time
            updated = True
        except (ValueError, TypeError):
            return jsonify({"message": "'tempo_espera' deve ser um número inteiro não negativo."}), 400

    if updated:
        return jsonify(hospital)
    else:
        return jsonify({"message": "Nenhum campo válido para atualização ('status' ou 'tempo_espera') foi fornecido."}), 400

# --- Execução no Google Colab ---
if __name__ == '__main__':
    FLASK_PORT = 5001
    print(f"Iniciando o servidor Flask na porta {FLASK_PORT}...")
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=False, use_reloader=False)
