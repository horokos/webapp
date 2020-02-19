import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    port="3310",
    user="root",
    password="haslo",
    database="pythonlogin"
)

mycursor = mydb.cursor()
username = "admin"
sql = "SELECT * FROM accounts WHERE username = " + username

print(sql)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
