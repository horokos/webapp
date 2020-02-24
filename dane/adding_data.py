import mysql.connector
from random import randint, choice

mydb = mysql.connector.connect(
    host="localhost",
    port="3310",
    user="root",
    password="haslo",
    database="pythonlogin"
)

mycursor = mydb.cursor()

colors = ['niebieski', 'czerwony', 'żółty', 'zielony', 'biały', 'czarny', 'różowy']

for i in range(1, 150):
    sql = "INSERT INTO `pythonlogin`.`rowery` (`id_roweru`, `id_modelu`, `rozmiar`, `kolor`) VALUES (NULL, %s, %s, %s);"
    var = [str(randint(1, 11)), str(randint(14, 22)) + '"', choice(colors)]
    mycursor.execute(sql, var)

for i in range(1, 12):
    sql = "INSERT INTO `pythonlogin`.`modele` " \
          "(`id_modelu`, `nazwa_modelu`, `typ_roweru`, `producent`, `wyposazenie`, `id_kat_cenowej`) " \
          "VALUES (NULL, %s, %s, %s, %s, %s);"
    var = ['model_' + str(randint(1, 10)), 'typ_' + str(randint(1, 2)), 'producent_' + str(randint(1, 4))]
    wyp = ''
    for j in range(1, 8):
        if randint(0, 1):
            wyp += 'wyp_' + str(j) + ', '
    var.append(wyp)
    var.append(str(randint(1, 6)))
    mycursor.execute(sql, var)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
