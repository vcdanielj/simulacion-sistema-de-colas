from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("/home.html")


@app.route("/colas-con-servidores-finitos")
def exercise1():
    return render_template("/exercise5.html")


@app.route("/colas-con-tiempos-de-servicio-variables")
def exercise2():
    return render_template("/exercise6.html")


if __name__ == "__main__":
    app.run(debug=True, port=4000)
