from flask import redirect, render_template, request, session, make_response
from app import app
import userhandling,advertisementQuery

@app.route("/")
def index():
    return render_template("index.html" )
@app.route("/profile")
#######################################################
# handle user#
def profile():
    return render_template("profile.html")
@app.route("/signin")

def registerUser():
    return render_template("signin.html")

@app.route("/register", methods=["POST"])

def register():
    userhandling.register(request.form["username"], request.form["password"]) 
    return redirect("/login") 

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
    user = userhandling.login(username, password)

    if user != None:
        session["username"] = username
        session["id"] = userhandling.id(username) 
        return redirect("/")
    return redirect("/loginerror")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

########################################################
### handle uploading

@app.route("/create")
def create():
    incomplete= advertisementQuery.getIncomplete(session["username"])
    advertisement_id ="" 
    header = "" 
    text = "" 
    images=""
    if incomplete:
        advertisement_id = incomplete[0]
        header = incomplete[4] 
        text = incomplete[5] 
        images=advertisementQuery.fetchImages(advertisement_id)

    return render_template("create.html",header=header, text=text, images= images, incomplete=incomplete, advertisement_id=advertisement_id)

@app.route("/newAdvertisement", methods=["POST"])
def newAdvertisement():
    advertisementQuery.newAdvertisement(session["id"])
    return redirect("/create")

@app.route("/remove", methods=["POST"])
def removeAdvertisement():
    advertisement_id = request.form["id"]
    #advertisementQuery.remove(adveretisement_id, session["id"])
    print("remove "+str(advertisement_id))
    return redirect("/create")

@app.route("/edit", methods=["POST"])
def edit():
    id = request.form["id"]
    if "publish" in request.form:
        print("publish")    

    if "upload" in request.form:
        text = request.form["text"]
        file = request.files["image"]
        advertisementQuery.send( text, id, file)

    if "delete" in request.form:
        advertisementQuery.removeAdvertisement(id) 
    return redirect("/create")

@app.route("/show/<int:id>")
def send(id):
    data = advertisementQuery.show(id)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response
