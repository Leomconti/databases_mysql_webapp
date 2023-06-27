import pymysql
from datetime import datetime

class Db:
    def __init__(self, host, database, user, password) -> None:
        self.db, self.dbc = self.open_connection(host, database, user, password)
    
    def open_connection(self, host: str, database: str, user: str, password: str):
        global conn_cursor, conn
        conn = None
        try:
            conn = pymysql.connect(
                host=host,
                user=user,
                passwd=password,
                database=database
            )

            conn_cursor = conn.cursor()
            return conn_cursor, conn
        except Exception as err:
            print(err)
            return [False, str(err)]

    def close_connection(self, host):
        conn.close()
        return [True, "Conexão fechada!"]


    def run_query(self, query: str):
        cursor = None
        try:
            cursor = self.db
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
            # Access row data using index or column names
                print(row)
            cursor.close()
            return rows
        except Exception as e:
            result = str(e)
            return False, result
        finally:
            cursor.close()
                
    def insert_pagamento(self, payerId: int, paymentDate: datetime, receipt: bytes, referenceYear: int, referenceMonth: int, unitId: int):
        cursor = self.db
        paymentDate = paymentDate.strftime('%Y-%m-%d')
        cursor.callproc('InsertPagamento', (payerId, paymentDate, receipt, referenceYear, referenceMonth, unitId))
        self.dbc.commit()

    def add_unit(self,id, location):
        cursor = self.db
        sql = "INSERT INTO Unidade (numero_identificador, localizacao) VALUES (%s, %s)"
        values = (id, location)
        cursor.execute(sql, values)
        self.dbc.commit()
    
    def add_payer(self,name,email,docId,phone):
        cursor = self.db
        sql = "INSERT INTO Pagador (nome_completo, email_contato, num_documento_identificacao, telefone_contato) VALUES (%s, %s, %s, %s)"
        values = (name,email,docId,phone)
        cursor.execute(sql, values)
        self.dbc.commit()


    def add_payment(self,payerId, payedDate,docPayed,yearRef, mesRef, unitId, regData):
        cursor = self.db
        sql = "INSERT INTO Pagamento (pagador_id, data_pagamento, comprovante, ano_referencia, mes_referencia, unidade_id, data_registro) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (payerId, payedDate,docPayed, yearRef, mesRef, unitId, regData)
        cursor.execute(sql, values)
        self.dbc.commit()

    def get_payers(self):
        cursor = self.db
        sql = "SELECT * FROM Pagador"
        cursor.execute(sql)
        result = cursor.fetchall()
        #print(result)
        return result
    
    def get_units(self):
        cursor = self.db
        sql = "SELECT * FROM Unidade"
        cursor.execute(sql)
        result = cursor.fetchall()
        #print(result)
        return result
    
    def get_payments(self):
        cursor = self.db
        sql = "SELECT * FROM Pagamento"
        cursor.execute(sql)
        result = cursor.fetchall()
        #print(result)
        return result