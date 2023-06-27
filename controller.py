# from mysql import Db

# db = Db("localhost", "condomManager", "admin", "admin123")


# # Every update in the database, this function will be called
# def update_csv_file():
#     column_names, rows = db.run_query("SELECT * FROM condomManager.pagamento;")
#     with open("teste.csv", "w") as f:
#         f.write(",".join(column_names) + "\n")
#         for row in rows:
#             f.write(",".join([str(i) for i in row]) + "\n")
#     f.close()