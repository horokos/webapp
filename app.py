from flask import Flask, render_template, request, redirect, url_for, session
import re

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


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
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


@app.route("/register", methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
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
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
            mydb.commit()
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)


@app.route("/bikes")
def bikes():
    return render_template('bikes.html')


@app.route("/info")
def info():
    return render_template('info.html')


@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'loggedin' in session:
        cursor = mydb.cursor()
        if request.method == 'POST' and 'username' in request.form:
            username = request.form['username']
            if username:
                cursor.execute("UPDATE accounts SET username = %s WHERE id = %s", [username, session['id']])
                mydb.commit()
                session['username'] = username
        if request.method == 'POST' and 'password' in request.form:
            password = request.form['password']
            if password:
                cursor.execute("UPDATE accounts SET password = %s WHERE id = %s", [password, session['id']])
                mydb.commit()
        if request.method == 'POST' and 'email' in request.form:
            email = request.form['email']
            if email:
                cursor.execute("UPDATE accounts SET email = %s WHERE id = %s", [email, session['id']])
                mydb.commit()
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
