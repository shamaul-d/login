from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def log():
    return render_template("login.html")    

@app.route("/auth", methods=["POST"])
def auth():
    user = "sham"
    pas = "shammy"
    res = "TRAITOR"
    if user == request.form['user'] and pas == request.form['pass']:
        res = "CONGRATS"
    return render_template("results.html", result = res)


if __name__ == "__main__":
    app.debug = True
    app.run()
