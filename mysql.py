import pymysql
from datetime import datetime

class Db:
    def __init__(self, host, database, user, password) -> None:
        db = self.open_connection(host, database, user, password)
    
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
            return conn_cursor
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
            column_names = [i[0] for i in cursor.description]
            cursor.close()
            return column_names, rows
        except Exception as e:
            result = str(e)
            return False, result
        finally:
            cursor.close()
                
    def insert_pagamento(self, payerId: int, paymentDate: datetime, receipt: bytes, referenceYear: int, referenceMonth: int, unitId: int):
        cursor = self.db.cursor()
        paymentDate = paymentDate.strftime('%Y-%m-%d')
        cursor.callproc('InsertPagamento', (payerId, paymentDate, receipt, referenceYear, referenceMonth, unitId))
        self.db.commit()
        cursor.close()
