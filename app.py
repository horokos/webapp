from flask import Flask, render_template, request, redirect, url_for, session
import re
from math import ceil
from time import strptime

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    port="3310",
    user="root",
    password="haslo",
    database="pythonlogin"
)

app = Flask(__name__)

app.secret_key = 'veryverysecretkey'


def logged():
    try:
        session['loggedin']
    except KeyError:
        session['loggedin'] = False


@app.route("/")
@app.route("/index")
def index():
    logged()
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    logged()
    if not session['loggedin']:
        msg = ''
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            mycursor = mydb.cursor()
            mycursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
            account = mycursor.fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                return redirect(url_for('index'))
            else:
                msg = 'Incorrect username/password!'
        return render_template('login.html', msg=msg)
    else:
        return redirect(url_for('index'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    logged()
    if not session['loggedin']:
        msg = ''
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            imie = request.form['imie']
            nazwisko = request.form['nazwisko']
            telefon = request.form['telefon']
            miejscowosc = request.form['miejscowosc']
            kod_pocztowy = request.form['kod_pocztowy']
            ulica = request.form['ulica']
            dom = request.form['dom']
            mieszkanie = request.form['mieszkanie']
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM accounts WHERE username = '" + username + "'")
            accountuser = cursor.fetchone()
            cursor.execute("SELECT * FROM accounts WHERE email = '" + email + "'")
            accountemail = cursor.fetchone()
            if accountuser:
                msg = 'Username is used!'
            elif accountemail:
                msg = 'Email is used!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not re.match(r'^[\d]{2}-[\d]{3}$', kod_pocztowy):
                msg = 'Niepoprawny kod pocztowy'
            elif not username or not password or not email or not imie or not nazwisko or not telefon or not kod_pocztowy or not miejscowosc or not ulica  or not dom or not mieszkanie:
                msg = 'Please fill out the form!'
            else:
                cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
                mydb.commit()
                return redirect(url_for('login'))
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('register.html', msg=msg)
    else:
        return redirect(url_for('index'))


@app.route("/bikes")
@app.route("/bikes/<int:page>")
def bikes(page=1):
    logged()
    if session['loggedin']:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT COUNT(*) FROM modele;")
        k = mycursor.fetchall()[0][0]
        n = ceil(k / 3)
        if page > n:
            return redirect(url_for('bikes'))
        else:
            if page == 1:
                pages = ['1', '2', '3']
            elif page == n:
                pages = [str(page-2), str(page - 1), str(page)]
            else:
                pages = [str(page-1), str(page), str(page+1)]
            bikes_info = []
            b = [(page-1)*3+i for i in range(0, 3) if ((page-1)*3+i+1 < k)]
            mycursor.execute('SELECT * FROM pythonlogin.modele;')
            x = mycursor.fetchall()
            mycursor.execute('SELECT COUNT(id_roweru), id_modelu, rozmiar FROM pythonlogin.rowery GROUP BY id_modelu, rozmiar ORDER BY id_modelu;')
            sizes = mycursor.fetchall()
            mycursor.execute('SELECT COUNT(id_roweru), id_modelu, kolor FROM pythonlogin.rowery GROUP BY id_modelu, kolor ORDER BY id_modelu;')
            colors = mycursor.fetchall()
            mycursor.execute('SELECT * FROM pythonlogin.kat_cenowe;')
            prices = mycursor.fetchall()
            for i in b:
                bike = dict(name='', maker='', type='', sizes='', equipment='', colors='', price='', model_id='')
                info_bike = x[i]
                bike['model_id'] = info_bike[0]
                bike['name'] = info_bike[1]
                bike['maker'] = info_bike[3]
                bike['type'] = info_bike[2]
                bike['equipment'] = info_bike[4]
                bike['price'] = prices[info_bike[5]-1][1] + ' zł za dzień'
                s = ''
                c = ''
                for j in sizes:
                    if j[1] == i+1:
                        s += j[2] + ', '
                bike['sizes'] = s
                for j in colors:
                    if j[1] == i+1:
                        c += j[2] + ', '
                bike['colors'] = c
                bikes_info.append(bike)
            return render_template('bikes.html', pages=pages, bikes=bikes_info)
    else:
        return redirect(url_for('login'))


@app.route("/info")
def info():
    logged()
    return render_template('info.html')


@app.route("/logout")
def logout():
    logged()
    if session['loggedin']:
        session['loggedin'] = False
        session.pop('id', None)
        session.pop('username', None)
        return redirect(url_for('index'))


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    logged()
    if session['loggedin']:
        cursor = mydb.cursor()
        changed = False
        msg = []
        if request.method == 'POST':
            username = request.form['username']
            if username:
                cursor.execute("SELECT * FROM accounts WHERE username = '" + username + "'")
                account = cursor.fetchone()
                if account:
                    msg.append('Name is used!')
                else:
                    cursor.execute("UPDATE accounts SET username = %s WHERE id = %s", [username, session['id']])
                    mydb.commit()
                    session['username'] = username
                    changed = True
            password = request.form['password']
            if password:
                cursor.execute("UPDATE accounts SET password = %s WHERE id = %s", [password, session['id']])
                mydb.commit()
                changed = True
            email = request.form['email']
            if email:
                cursor.execute("SELECT * FROM accounts WHERE email = '" + email + "'")
                account = cursor.fetchone()
                if account:
                    msg = 'Email is used!'
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid email address!'
                else:
                    cursor.execute("UPDATE accounts SET email = %s WHERE id = %s", [email, session['id']])
                    mydb.commit()
                    changed = True
            imie = request.form['imie']
            if imie:
                cursor.execute("UPDATE accounts SET imie = %s WHERE id = %s", [imie, session['id']])
                mydb.commit()
                changed = True
            nazwisko = request.form['nazwisko']
            if nazwisko:
                cursor.execute("UPDATE accounts SET nazwisko = %s WHERE id = %s", [nazwisko, session['id']])
                mydb.commit()
                changed = True
            telefon = request.form['telefon']
            if telefon:
                cursor.execute("UPDATE accounts SET telefon = %s WHERE id = %s", [telefon, session['id']])
                mydb.commit()
                changed = True
            miejscowosc = request.form['miejscowosc']
            if miejscowosc:
                cursor.execute("UPDATE accounts SET miejscowosc = %s WHERE id = %s", [miejscowosc, session['id']])
                mydb.commit()
                changed = True
            kod_pocztowy = request.form['kod_pocztowy']
            if kod_pocztowy:
                if not re.match(r'^[\d]{2}-[\d]{3}$', kod_pocztowy):
                    cursor.execute("UPDATE accounts SET kod_pocztowy = %s WHERE id = %s", [kod_pocztowy, session['id']])
                    mydb.commit()
                    changed = True
                else:
                    msg = 'Niepoprawny kod pocztowy'
            ulica = request.form['ulica']
            if ulica:
                cursor.execute("UPDATE accounts SET ulica = %s WHERE id = %s", [ulica, session['id']])
                mydb.commit()
                changed = True
            dom = request.form['dom']
            if dom:
                cursor.execute("UPDATE accounts SET dom = %s WHERE id = %s", [dom, session['id']])
                mydb.commit()
                changed = True
            mieszkanie = request.form['mieszkanie']
            if mieszkanie:
                cursor.execute("UPDATE accounts SET mieszkanie = %s WHERE id = %s", [mieszkanie, session['id']])
                mydb.commit()
                changed = True
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account, msg=msg, changed=changed)
    return redirect(url_for('login'))


@app.route("/pick", methods=['GET', 'POST'])
@app.route("/pick?<int:model_id>", methods=['GET', 'POST'])
def pick(model_id=None):
    logged()
    if session['loggedin']:
        msg = ''
        if model_id is not None:
            if request.method == 'POST' and 'start_date' in request.form and 'end_date' in request.form and not 'bike' in request.form:
                start_date = request.form['start_date']
                end_date = request.form['end_date']
                sd = strptime(start_date, '%Y-%m-%d')
                ed = strptime(end_date, '%Y-%m-%d')
                if not start_date or not end_date:
                    msg = 'Wybierz daty'
                    return render_template('pick.html', msg=msg, model_id=model_id)
                elif sd > ed:
                    msg = 'Wybierz poprawne daty'
                    return render_template('pick.html', msg=msg, model_id=model_id)
                else:
                    dates = [start_date, end_date]
                    mycursor = mydb.cursor()
                    mycursor.execute('SELECT * FROM pythonlogin.rowery WHERE id_modelu=%s ORDER BY rozmiar', [model_id])
                    b = mycursor.fetchall()
                    mycursor.execute(
                        'SELECT * FROM pythonlogin.zamowienia WHERE data_poczatkowa BETWEEN %s AND %s OR data_koncowa BETWEEN %s AND %s',
                        [start_date, end_date, start_date, end_date])
                    o = mycursor.fetchall()
                    for i in o:
                        for j in b:
                            if i[2] == j[0]:
                                b.remove(j)
                    bikes_info = b
                    return render_template('pick.html', dates=dates, bikes=bikes_info, msg=msg, model_id=model_id)
            elif request.method == 'POST' and 'bike' in request.form:
                mycursor = mydb.cursor()
                mycursor.execute('INSERT INTO pythonlogin.zamowienia VALUES (NULL, %s, %s, %s, %s)',
                                 [session['id'], request.form['bike'], request.form['start_date'], request.form['end_date']])
                mydb.commit()
                return redirect(url_for('orders'))
            else:
                return render_template('pick.html', model_id=model_id)
        else:
            return redirect(url_for('bikes'))
    else:
        return redirect(url_for('login'))


@app.route("/orders")
def orders(msg=False):
    logged()
    if session['loggedin']:
        mycursor = mydb.cursor()
        mycursor.execute('SELECT zamowienia.id_zamowienia, modele.nazwa_modelu, rowery.rozmiar, rowery.kolor, zamowienia.data_poczatkowa, zamowienia.data_koncowa\
                        FROM zamowienia\
                        INNER JOIN rowery ON zamowienia.id_roweru=rowery.id_roweru\
                        INNER JOIN modele ON rowery.id_modelu=modele.id_modelu\
                        WHERE zamowienia.id_klienta=%s;', [session['id']])
        o = mycursor.fetchall()
        return render_template('orders.html', orders=o)


if __name__ == '__main__':
    app.run(debug=True)
