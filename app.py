import os
import io
import time
from flask import Flask, send_file, render_template, request
from mysql import Db

app = Flask(__name__)

HOST = "localhost"
DATABASE = "condomManager"
USER = "root"
PASSWORD = "admin123"
db = Db(HOST, DATABASE, USER, PASSWORD)

# Routes for views
@app.route('/')
def home():
    # O que esta em array tem que ser pego do banco de dados
    # quer pra puxar id e nome de unidade e pagador, da um jeito de organizar em lista zipada
    # TODO: ARTHUR
    pagadores = db.get_payers()
    unidades = db.get_units()
    pagador_ids = []
    for row in pagadores:
        pagador_ids.append(row[0])
    pagador_nomes = []
    for row in pagadores:
        pagador_nomes.append(row[1])
    unidade_ids = []
    for row in unidades:
        unidade_ids.append(row[0])
    unidade_nomes = []
    for row in unidades:
        unidade_nomes.append(row[2])
    pagadores = list(zip(pagador_ids, pagador_nomes))
    unnidades = list(zip(unidade_ids, unidade_nomes))
    return render_template('views/home.html', pagadores = pagadores, unidades = unnidades)

@app.route('/pagamentos')
def pagamentos():
    
    resultado = db.get_payments()
    column_names = ["payment_id", "pagador_id", "data_pagamento", "comprovante", "ano_referencia", "mes_referencia", "unidade_id", "data_registro"]
    rows = []

    for row in resultado:
        rows.append(row)
    
    return render_template('views/pagamento.html', column_names=column_names, rows=rows)

@app.route('/unidades')
def unidade():
    return render_template('views/unidade.html')

@app.route('/pagadores')
def pagadores():
    return render_template('views/pagador.html')


# FUNCOES PARA ADICIONAR NO BANCO DE DADOS ETC

# TODO: ARTHUR
@app.route('/add_pagador', methods=['POST'])
def add_pagador():
    nome_completo = request.form.get('nome_completo')
    email_contato = request.form.get('email_contato')
    num_documento_identificacao = request.form.get('num_documento_identificacao')
    telefone_contato = request.form.get('telefone_contato')
    
    # querys para insert 
    db.add_payer(nome_completo, email_contato, num_documento_identificacao, telefone_contato)
    return render_template('views/success.html')

# TODO: ARTHUR
@app.route('/add_unidade', methods=['POST'])
def add_unidade():
    numero_identificador = request.form.get('numero_identificador')
    localizacao = request.form.get('localizacao')

    db.add_unit(numero_identificador, localizacao)
    return render_template('views/success.html')

# TODO: ARHUR
@app.route('/add_payment', methods=['POST'])
def add_payment():
    pagador_id = request.form.get('pagador_id')
    data_pagamento = request.form.get('data_pagamento')
    comprovante = request.files['comprovante'].read()
    ano_referencia = request.form.get('ano_referencia')
    mes_referencia = request.form.get('mes_referencia')
    unidade_id = request.form.get('unidade_id')
    
    db.add_payment(pagador_id, data_pagamento, comprovante, ano_referencia, mes_referencia, unidade_id, time.strftime('%Y-%m-%d %H:%M:%S'))
    
    return render_template('views/success.html')

# TODO: ARTHUR
@app.route('/download_comprovante/<int:payment_id>')
def download_comprovante(payment_id):
    # Aqui catar comprovante
    # query = f"SELECT comprovante FROM Pagamento WHERE payment_id = {payment_id}"
    # comprovante = db.run_query(query)
    comprovante = b'BANANA'

    return send_file(path_or_file=io.BytesIO(comprovante),
                     as_attachment=True,
                     download_name=f'comprovante_{payment_id}.pdf'
                     )

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(port=5000)
