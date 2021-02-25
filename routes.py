from flask import redirect, render_template, request, session, make_response
from app import app
import userhandling,advertisementQuery

@app.route("/")
def index():
    return render_template("index.html" )

@app.route("/profile")
def profile():
    ## fetch profiles published advertisements
    ## fetch images of advertisements
    advertisements = advertisementQuery.getPublishedAdvertisements(session["id"])
    images =[]  
    if advertisements != None: 
        for adv in advertisements:
            id = adv[0]
            images.append(advertisementQuery.fetchImages(adv[0]))
    
    return render_template("profile.html", advertisements = advertisements, images = images)

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
    del session["id"]
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
    for ids in incomplete_ids:
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

    return render_template("edit.html",header=advertisement[4], images = images, text = advertisement[6], price = advertisement[5], advertisement_id = id)

@app.route("/delete/<int:id>")
def delete(id):
    advertisementQuery.removeAdvertisement(id,session["id"])
    return redirect("/create")

@app.route("/handleRedirect", methods=["POST"])
def handle():
    advertisement_id = request.form["id"]
    if "delete" in request.form:
        return redirect("/delete/"+str(advertisement_id)) 
    if "edit" in request.form:
        return redirect("/editAdvertisement/"+str(advertisement_id))
@app.route("/updateAdvertisement", methods=["POST"])
def modify():
    id = request.form["id"]
    content= request.form["text"]
    header = request.form["header"]
    price = request.form["price"]

    advertisementQuery.updateContent(content, header, price, id)    

    if "publish" in request.form:
        print("publish")
        advertisementQuery.publish(id, session["id"])
        return redirect("/show/advertisement/"+str(id))
    if "upload" in request.form:
        print("upload image")
        file = request.files["image"]
        advertisementQuery.sendimage(id, file)

    return redirect("/editAdvertisement/"+str(id))

@app.route("/show/advertisement/<int:id>")
def show_advertsiment(id):
    advertisement=advertisementQuery.get_advertisement(id)
    images = advertisementQuery.fetchImages(id)

    return render_template("advertisement.html", header=advertisement[4], images = images, text = advertisement[6], price = advertisement[5], advertisement_id = id)

@app.route("/show/<int:id>")
def send_img(id):
    data = advertisementQuery.show_img(id)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response
