import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    port="3310",
    user="root",
    password="haslo",
    database="pythonlogin"
)

mycursor = mydb.cursor()
mycursor.execute('SELECT * FROM pythonlogin.rowery WHERE id_modelu=4')
bikes = mycursor.fetchall()
mycursor.execute('SELECT * FROM pythonlogin.zamowienia WHERE data_poczatkowa BETWEEN %s AND %s OR data_koncowa BETWEEN %s AND %s', ['2020-02-23', '2020-02-24', '2020-02-23', '2020-02-24'])
orders = mycursor.fetchall()

print(bikes)
print(orders)
