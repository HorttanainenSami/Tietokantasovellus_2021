from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] =getenv("DATABASE_URL") 
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html" ) 
@app.route("/profile")
def profile():
    return render_template("profile.html")
@app.route("/signin")
def registerUser():
    #siirretään uuden tilin kirjautumis sivulle
    return render_template("signin.html")

@app.route("/register", methods=["POST"])
def register():
    ## lisää tietokantaan tili
    # lisää tietokantaan salasana ja käyttäjä
    # muista encryptata salasana 
    username=request.form["username"]
    hash_value = generate_password_hash(request.form["password"])
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password" : hash_value})
    db.session.commit() 
    return redirect("/") 
@app.route("/create")
def create():
    return(render_template("create.html"))

@app.route("/login")
def login():
    return(render_template("login.html"))

@app.route("/loginerror")
def result():
    return(render_template("loginerror.html"))

@app.route("/checklogin", methods=["POST"])
def checklogin():
    username=request.form["username"]
    password=request.form["password"]

    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username}) 
    user = result.fetchone()

    if user == None:
        # wrong password or username 
        return redirect("/loginerror")
    else:
        #correct username
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            # correct username and password, login
            session["username"]=username
        else:
            #incorrect password
            return redirect("/loginerror")

    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
