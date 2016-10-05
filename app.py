from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

@app.route("/", methods=["GET"])
def log():
    i = 0
    for arg in request.args:
        i += 1
    if i == 0:
        stat = ""
    elif request.args["nuser"] == "" or request.args["npass"] == "":
        stat = "Please fill in all forms of information."
    elif not check(request.args["nuser"]):
        stat = "Username already taken!"
    else:
        add(request.args["nuser"],request.args["npass"])
        stat = "New account created."
    return render_template("login.html", status = stat)    

@app.route("/auth", methods=["POST"])
def auth():
    m = master()
    print m
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
