from flask import Flask, render_template, url_for


app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/register")
def register():
    return render_template('register.html')


@app.route("/bikes")
def bikes():
    return render_template('bikes.html')


@app.route("/info")
def info():
    return render_template('info.html')


if __name__ == '__main__':
    app.run(debug=True)
