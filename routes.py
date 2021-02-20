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
    incompletes= advertisementQuery.getIncompletes(session["id"])
    incomplete_ids = []
    images =[]
    for incomplete in incompletes:
        incomplete_ids.append(incomplete[0])
    for i, ids in enumerate(incomplete_ids):
        result = advertisementQuery.fetchImages(ids)
        images.append(result) 
    return render_template("create.html",incompletes=incompletes, images = images)

@app.route("/newAdvertisement", methods=["POST"])
def newAdvertisement():
    advertisement_id = advertisementQuery.newAdvertisement(session["id"])
    return redirect("/editAdvertisement/"+str(advertisement_id))
#############
@app.route("/editAdvertisement/<int:id>", methods =["GET"])
def editAdvertisement(id):
    images = advertisementQuery.fetchImages(id)  
    advertisement = advertisementQuery.getIncomplete(session["id"], id)

    return render_template("edit.html",header=advertisement[4], images = images, text = advertisement[5], advertisement_id = id)

@app.route("/delete", methods=["POST"])
def delete():
    id = request.form["id"]
    if "delete" in request.form:
        advertisementQuery.removeAdvertisement(id) 
    return redirect("/create")

@app.route("/edit", methods=["POST"])
def edit():
    id = request.form["id"]
    content= request.form["text"]
    header = request.form["header"]
    advertisementQuery.updateContent(content, header, id)    

    if "publish" in request.form:
        print("publish")
    if "upload" in request.form:
        print("upload image")
        file = request.files["image"]
        advertisementQuery.sendimage(id, file)

    return redirect("/editAdvertisement/"+str(id))

@app.route("/show/<int:id>")
def send(id):
    data = advertisementQuery.show(id)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response
