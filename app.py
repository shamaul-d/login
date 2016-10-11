from flask import Flask, render_template, request, session, url_for, redirect
import hashlib

app = Flask(__name__)
app.secret_key = '\xceY\x96\x0b^\x8d:\xea\xd2\x9c\xae\xf2\xfc\xdd\x8dL\xf5Dsw\x8a\xcb=\xf8\xf1\xe5\x89K\xbd\x17\x1eg'

@app.route("/")
def log():
    return render_template("login.html", status = "")

@app.route("/auth", methods=["POST"])
def auth():
    i = 0
    for arg in request.form:
        i += 1 
    if i == 0:
        return render_template("login.html", status = "")
    if "reg" in request.form: 
        if request.form["user"] == "" or request.form["pass"] == "":
            stat = "Please fill in all forms of information."
        elif not check(request.form["user"]):
            stat = "Username already taken!"
        else:
            add(request.form["user"],request.form["pass"])
            stat = "New account created."
        return render_template("login.html", status = stat)
    m = master()
    user = request.form['user']
    if check(user):
        res = "Username does not exist!"
    else:
        pas = m[user]
        if pas == hashlib.sha512(request.form['pass']).hexdigest() + "\n":
            res = "Log in successful."
        else:
            res = "Password is incorrect."
    return render_template("results.html", result = res)

def add(user, password):
    old = open("data/passwords.csv", "r")
    master = ""
    for row in old:
        master += row
    old.close()
    new = open("data/passwords.csv", "w")
    new.write(master)
    new.write(user)
    new.write(",")
    new.write(hashlib.sha512(password).hexdigest())
    new.write("\n")
    new.close()

def check(user):
    old = open("data/passwords.csv", "r")
    f = old.readline()
    while f != "":
        if f.find(user) != -1:
            return False
        f = old.readline()
    return True

def master():
    ma = open("data/passwords.csv","r")
    l = []
    for row in ma:
        l.append(row)
    ma.close()
    d = {}
    for i in l:
        c = i.rfind(",")
        d[i[0:c]] = i[c+1:len(i)]
    return d

if __name__ == "__main__":
    app.debug = True
    app.run()
