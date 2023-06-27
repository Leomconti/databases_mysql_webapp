import os
import io
from flask import Flask, send_file, render_template, request
from mysql import Db
# from controller import update_csv_file
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
    pagador_ids = [101, 102, 103, 104, 105]
    pagador_nomes = ["João", "Maria", "José", "Pedro", "Ana"]
    unidade_ids = [1001, 1002, 1003, 1004, 1005]
    unidade_nomes = ["Apto 101", "Apto 102", "Apto 103", "Apto 104", "Apto 105"]
    
    return render_template('views/home.html', pagadores = list(zip(pagador_ids, pagador_nomes)), unidades = list(zip(unidade_ids, unidade_nomes)))

@app.route('/pagamentos')
def pagamentos():
    # -- QUERY AQUI!!!! --
    # column_names, rows = db.run_query("SELECT * FROM condomManager.pagamento;")
    # O que esta em array tem que ser pego do banco de dados
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

@app.route('/add_pagador', methods=['POST'])
def add_pagador():
    # querys para insert
    return render_template('views/success.html')


@app.route('/add_unidade', methods=['POST'])
def add_unidade():
    # querys para insert
    return render_template('views/success.html')


@app.route('/add_payment', methods=['POST'])
def add_payment():
    pagador_id = request.form.get('pagador_id')
    data_pagamento = request.form.get('data_pagamento')
    comprovante = request.files['comprovante'].read()
    ano_referencia = request.form.get('ano_referencia')
    mes_referencia = request.form.get('mes_referencia')
    unidade_id = request.form.get('unidade_id')
    
    # testar o insert aqui
    # db.insert_pagamento(pagador_id, data_pagamento, comprovante, ano_referencia, mes_referencia, unidade_id)
    
    return render_template('views/success.html')

@app.route('/download_comprovante/<int:payment_id>')
def download_comprovante(payment_id):
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
