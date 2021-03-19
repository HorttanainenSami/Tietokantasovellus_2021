from flask import redirect, render_template, request, session, make_response, url_for, flash
from app import app
import userSession, query, chat
from datetime import datetime, timedelta

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/user/messages")
def show_all_chats():
    chats = chat.get_all(session["id"])
    def format_date(date):
        time_passed = datetime.now()-date
        if timedelta(days=1) > time_passed:
            return date.strftime('%X')
        else:
            return date.strftime('%d/%m/%y %X')
    return render_template("chats.html", active_chats=chats, format_date=format_date)

@app.route("/chat/<int:chat_id>")
def show_chat(chat_id):
    ## check authority to participate in chat
    messages = chat.get_messages(chat_id, session["id"])
    if not messages:
        return render_template('404.html'), 404
    profile_info = chat.get_participant(chat_id, session['id'])  

    print(profile_info)
    print(type(profile_info[2]))
    def format_date(date):
        time_passed = datetime.now()-date
        if timedelta(days=1) > time_passed:
            return date.strftime('%X')
        else:
            return date.strftime('%d/%m/%y %X')

    return render_template("chat.html", messages=messages, chat_id=chat_id, formatdate=format_date, profile=profile_info)

@app.route("/chat/create", methods=["POST"])
def chat_create():
    advertisement_id = request.form["advertisement_id"]
    message = request.form["message"]

    ## check if already active chat
    chat_id = chat.get_active(session['id'], advertisement_id)
    if chat_id:
        #chat_send_message
        chat_id = chat_id[0]
        chat.message_send(chat_id, message, session['id'])
    else:
        #chat_create_new
        chat_id = chat.create(session["id"], advertisement_id, message)

    return redirect("/chat/"+str(chat_id))

@app.route("/chat/sendmessage", methods=["POST"])
def message_send():
    message = request.form['message']
    print(message)
    chat_id = request.form['chat_id']
    print(chat_id)
    chat.message_send(chat_id, message, session['id'])
    return redirect('/chat/'+str(chat_id))

##UserSession handling
@app.route("/user/profile")
def profile():
    profile = userSession.get_user(session['id'])
    pub_adv = query.get_advert_published(session["id"])

    def get_images(advertisement_id):
        images = query.get_images(advertisement_id)
        return images

    return render_template("profile.html", advertisements=pub_adv, get_images=get_images, profile = profile)

@app.route('/user/profile/<int:user_id>')
def show_profile(user_id):
    profile = userSession.get_user(user_id)
    pub_adv = query.get_advert_published(user_id)

    def get_images(advertisement_id):
        images = query.get_images(advertisement_id)
        return images

    return render_template("profile.html", advertisements=pub_adv, get_images=get_images, profile=profile)

@app.route('/user/profile/remove', methods=['POST'])
def profile_delete():
    ## DELETE ALL 
    return 

@app.route('/user/profile/changepassword')
def profile_change_password_form():
    return render_template('change_password.html')

@app.route('/user/profile/modify')
def profile_modify():
    profile = userSession.get_user(session['id'])
    return render_template('profile_modify.html', profile=profile)

@app.route('/user/changepassword', methods=['POST'])
def profile_change_password():
    old = request.form['old_password']
    new = request.form['new_password']
    result = userSession.change_password(old, new, session['id'])

    if 'error' in result:
        flash('Salasanasi oli väärin', 'error')
        return render_template('change_password.html')
    
    flash('Salasanasi on vaihdettu', 'success')
    return redirect('/user/profile')

@app.route('/user/profile/avatar/remove', methods=['POST'])
def remove_avatar():
    userSession.avatar_remove(session['id'])
    return redirect('/user/profile/modify')

@app.route('/user/profile/update', methods= ['POST'])
def update_profile():
    if 'file' in request.files:
        file = request.files['file']
        print(file)
        userSession.avatar_save(session['id'], file)

    pitch = request.form['pitch']
    reside = request.form['reside']
    userSession.update(pitch, reside, session['id'])
    return redirect('/user/profile/modify') 

@app.route('/user/profile/<int:id>')
def profile_show(id):
    profile = userSession.get_user(session['id'])
    return render_template('profile.html', profile=profile)

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    result = userSession.handleRegister(username, password)
    if 'error' in result:
        flash('Käyttäjätunnus on jo käytössä', 'error')
        return redirect('/signin')
    flash('Käyttäjätunnus on luotu, kirjaudu nyt sisään', 'success')
    return redirect("/login")

@app.route("/login", methods=["POST", "GET"])
def login():
    if "recentUrl" in request.form:
        session["url"] = request.form["recentUrl"]
    return render_template("login.html")

@app.route("/login/check", methods=["POST"])
def checklogin():
    username = request.form["username"]
    password = request.form["password"]
    user = userSession.handleLogin(username, password)

    if user:
        session["username"] = user[1]
        session["id"] = user[0]
        flash('Tervetuloa, '+str(session['username']), 'success')
        if 'url' in session:
            url = session['url']
            del session['url']
            return redirect(url)
        return redirect("/")
    flash('Käyttäjä ja/tai salasana väärin', 'error')
    return redirect("/login")

@app.route("/logout")
def logout():
    del session["username"]
    del session["id"]
    flash('Olet kirjautunut ulos, nähdään taas pian :)', 'success')
    return redirect("/")

########################################################
### handle uploading

@app.route("/")
def index():
    advertisements = query.get_adverts()
    images = []
    for adv in advertisements:
        images.append(query.get_images(adv[0]))
        print(images)
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
