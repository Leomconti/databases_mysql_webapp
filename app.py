import os
import io
from flask import Flask, send_file, render_template, request
from mysql import Db

app = Flask(__name__)

HOST = "localhost"
DATABASE = "condomManager"
USER = "admin"
PASSWORD = "admin123"
db = Db(HOST, DATABASE, USER, PASSWORD)

# Routes for views
@app.route('/')
def home():
    # O que esta em array tem que ser pego do banco de dados
    # query pra puxar id e nome de unidade e pagador, da um jeito de organizar em lista zipada
    # TODO: ARTHUR
    pagador_ids = [101, 102, 103, 104, 105]
    pagador_nomes = ["João", "Maria", "José", "Pedro", "Ana"]
    unidade_ids = [1001, 1002, 1003, 1004, 1005]
    unidade_nomes = ["Apto 101", "Apto 102", "Apto 103", "Apto 104", "Apto 105"]
    pagadores = list(zip(pagador_ids, pagador_nomes))
    unnidades = list(zip(unidade_ids, unidade_nomes))
    return render_template('views/home.html', pagadores = pagadores, unidades = unnidades)

@app.route('/pagamentos')
def pagamentos():
    # -- QUERY AQUI!!!! --
    # TODO: ARTHUR
    # column_names, rows = db.run_query("SELECT * FROM condomManager.pagamento;")
    # O que esta em array tem que ser pego do banco de dados
    # Literal so testar a qeury ali de cima
    column_names = ["payment_id", "pagador_id", "data_pagamento", "comprovante", "ano_referencia", "mes_referencia", "unidade_id", "data_registro"]
    rows = [
        [1, 101, '2023-01-01', 'Sample comprovante 1', 2023, 1, 1001, '2023-01-01 10:00:00'],
        [2, 102, '2023-02-01', 'Sample comprovante 2', 2023, 2, 1002, '2023-02-01 11:00:00'],
        [3, 103, '2023-03-01', 'Sample comprovante 3', 2023, 3, 1003, '2023-03-01 12:00:00'],
        [4, 104, '2023-04-01', 'Sample comprovante 4', 2023, 4, 1004, '2023-04-01 13:00:00'],
        [5, 105, '2023-05-01', 'Sample comprovante 5', 2023, 5, 1005, '2023-05-01 14:00:00']
    ]
    
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

    return render_template('views/success.html')

# TODO: ARTHUR
@app.route('/add_unidade', methods=['POST'])
def add_unidade():
    numero_identificador = request.form.get('numero_identificador')
    localizacao = request.form.get('localizacao')

    # querys para insert
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
    
    
    # TODO: ARTHUIR - TESTAR ETC, SO COLOQUEI
    # db.run_query(f"INSERT INTO condomManager.pagamento (pagador_id, data_pagamento, comprovante, ano_referencia, mes_referencia, unidade_id) VALUES ({pagador_id}, {data_pagamento}, {comprovante}, {ano_referencia}, {mes_referencia}, {unidade_id});")
    # testar o insert aqui   -- tem que ser procedure, no back ta como procedure ok
    # db.insert_pagamento(pagador_id, data_pagamento, comprovante, ano_referencia, mes_referencia, unidade_id)
    
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
