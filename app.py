import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Leitura da Feature Flag via variável de ambiente (Default: False/Desativado)
FEATURE_DESCONTO_PROMO = os.getenv("FEATURE_DESCONTO_PROMO", "false").lower() == "true"


@app.route('/')
def home():
    return jsonify({"mensagem": "Bem-vindo a API FastOrder!"})


@app.route('/api/status')
def status():
    return jsonify({
        "status": "operacional",
        "servico": "FastOrder-Web",
        "flags": {
            "desconto_promo": FEATURE_DESCONTO_PROMO
        }
    })


@app.route('/api/soma')
def soma():
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
        return jsonify({"resultado": a + b})
    except (ValueError, TypeError):
        return jsonify({"erro": "Parametros invalidos"}), 400


@app.route('/api/desconto')
def desconto():
    if not FEATURE_DESCONTO_PROMO:
        return jsonify({
            "erro": "Funcionalidade em construcao ou desativada temporariamente",
            "flag_status": False
        }), 403
    try:
        valor_total = float(request.args.get('valor', 0))
        porcentagem = float(request.args.get('porcentagem', 10))

        if valor_total <= 0:
            return jsonify({"erro": "Valor deve ser maior que zero"}), 400

        valor_com_desconto = valor_total - (valor_total * (porcentagem / 100))

        return jsonify({
            "valor_original": valor_total,
            "desconto_aplicado": f"{porcentagem}%",
            "valor_final": valor_com_desconto
        })
    except (ValueError, TypeError):
        return jsonify({"erro": "Parametros de desconto invalidos"}), 400


if __name__ == '__main__':
    # A flag '# nosec B104' evita falsos positivos do Bandit ao fazer bind em 0.0.0.0
    app.run(host='0.0.0.0', port=5000)  # nosec B104
