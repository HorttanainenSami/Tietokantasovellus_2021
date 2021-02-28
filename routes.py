from flask import redirect, render_template, request, session, make_response, url_for
from app import app
import userSession, query

##UserSession handling
@app.route("/user/profile")
def profile():
    ## fetch profiles published advertisements
    ## fetch images of advertisements
    session['url'] = url_for('profile')
    pub_adv = query.get_advert_published(session["id"])
    images = []
    if pub_adv:
        for adv in pub_adv:
            images.append(query.get_images(adv[0]))

    return render_template("profile.html", advertisements=pub_adv, images=images)

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    userSession.handleRegister(username, password)
    return redirect("/login")

@app.route("/login", methods=["POST", "GET"])
def login():
    if "recentUrl" in request.form:
        session["url"] = request.form["recentUrl"]
    return render_template("login.html")

@app.route("/login/error")
def loginerror():
    return render_template("loginerror.html")

@app.route("/login/check", methods=["POST"])
def checklogin():
    username = request.form["username"]
    password = request.form["password"]
    user = userSession.handleLogin(username, password)

    if user:
        session["username"] = user[1]
        session["id"] = user[0]
        if 'url' in session:
            url = session['url']
            del session['url']
            return redirect(url)
        return redirect("/")

    return redirect("/login/error")

@app.route("/logout")
def logout():
    del session["username"]
    del session["id"]
    return redirect("/")

########################################################
### handle uploading

@app.route("/")
def index():
    advertisements = query.get_adverts()
    images = []
    for adv in advertisements:
        images.append(query.get_images(adv[0]))
    return render_template("index.html", images=images, advertisements=advertisements)

@app.route("/advertisement/unpublished")
def show_unpub_adv():
    incompletes = query.get_advert_incompletes(session["id"])
    images = []
    for incomplete in incompletes:
        advert_id = incomplete[0]
        result = query.get_images(advert_id)
        images.append(result)

    return render_template("create.html", advertisements=incompletes, images=images)

@app.route("/advertisement/new", methods=["POST"])
def new_adv():
    advertisement_id = query.advert_new(session["id"])
    return redirect("/advertisement/edit/"+str(advertisement_id))

@app.route("/advertisement/edit/<int:id>", methods=["GET"])
def edit_adv(id):
    images = query.get_images(id)
    advertisement = query.get_advert_incomplete(session["id"], id)

    return render_template("edit.html", header=advertisement[5], images=images, content=advertisement[7], price=advertisement[6], advertisement_id=id)

@app.route("/advertisement/delete/<int:id>")
def delete_adv(id):
    query.advert_remove(id, session["id"])

    if 'url' in session:
        url = session['url']
        del session['url']
        return redirect(url)

    return redirect("/")

@app.route("/handleRedirect", methods=["POST"])
def handle():
    advertisement_id = request.form["id"]

    if "delete" in request.form:
        session['url'] = request.form['url']
        return redirect("/advertisement/delete/"+str(advertisement_id))
    if "edit" in request.form:
        return redirect("/advertisement/edit/"+str(advertisement_id))

@app.route("/advertisement/update", methods=["POST"])
def update_adv():
    id = request.form["id"]
    content = request.form["text"]
    header = request.form["header"]
    price = request.form["price"]

    query.advert_update(content, header, price, id)

    if "publish" in request.form:
        print("publish")
        query.advert_publish(id, session["id"])
        return redirect("/show/advertisement/"+str(id))
    if "upload" in request.form:
        print("upload image")
        file = request.files["image"]
        query.image_save(id, file)

    return redirect("/advertisement/edit/"+str(id))

@app.route("/show/advertisement/<int:id>")
def show_adv(id):
    advertisement = query.get_advert(id)
    images = query.get_images(id)

    return render_template("advertisement.html", advertisement=advertisement, images=images)

@app.route("/show/image/<int:id>")
def show_img(id):
    data = query.image_show(id)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response
