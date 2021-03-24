from flask import redirect, render_template, request, session, make_response, url_for, flash
from app import app
import user, query, chat
from datetime import datetime, timedelta

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/user/messages')
def show_all_chats():
    chats = chat.get_all(session['id'])
    def format_date(date):
        time_passed = datetime.now()-date
        if timedelta(days=1) > time_passed:
            return date.strftime('%X')
        else:
            return date.strftime('%d/%m/%y %X')
    return render_template('chats.html', active_chats=chats, format_date=format_date)

@app.route('/chat/<int:chat_id>')
def show_chat(chat_id):
    ## check authority to participate in chat
    messages = chat.get_messages(chat_id, session['id'])
    if not messages:
        return render_template('404.html'), 404
    profile_info = chat.get_participant(chat_id, session['id'])  

    def format_date(date):
        time_passed = datetime.now()-date
        if timedelta(days=1) > time_passed:
            return date.strftime('%X')
        else:
            return date.strftime('%d/%m/%y %X')

    return render_template('chat.html', messages=messages, chat_id=chat_id, formatdate=format_date, profile=profile_info)

@app.route('/chat/create', methods=['POST'])
def chat_create():
    advertisement_id = request.form['advertisement_id']
    message = request.form['message']
    participant = request.form['user_id']

    ## check if already active chat
    chat_id = chat.get_active(session['id'], advertisement_id)
    if chat_id:
        #chat_send_message
        chat_id = chat_id[0]
        chat.send(chat_id, message, session['id'])
    else:
        #chat_create_new
        chat_id = chat.create(session['id'],participant, advertisement_id, message)

    return redirect('/chat/'+str(chat_id))

@app.route('/chat/sendmessage', methods=['POST'])
def send():
    message = request.form['message']
    chat_id = request.form['chat_id']
    chat.send(chat_id, message, session['id'])
    return redirect('/chat/'+str(chat_id))
##################################################################################################################################################################
##UserSession handling
@app.route('/user/profile/<int:user_id>')
def show_profile(user_id):
    profile = user.get_user(user_id)
    published = query.get_published(user_id)

    images = []
    for adv in published:
        advert_id = adv[0]
        result = query.get_images(advert_id)
        images.append(result)

    return render_template('profile.html', advertisements=published,images=images,  profile=profile)

@app.route('/user/profile/remove', methods=['POST'])
def profile_delete():
    user.remove_user(session['id'])
    del session['id']
    del session['username']
    flash('Käyttäjätunnuksesi on poistettu','success')
    return redirect('/') 

@app.route('/user/profile/changepassword')
def profile_change_password_form():
    if 'id' not in session:
        return redirect('/login')
    return render_template('change_password.html')

@app.route('/user/profile/modify')
def profile_modify():
    profile = user.get_user(session['id'])
    return render_template('profile_modify.html', profile=profile)

@app.route('/user/changepassword', methods=['POST'])
def profile_change_password():
    old = request.form['old_password']
    new = request.form['new_password']
    result = user.change_password(old, new, session['id'])

    if 'error' in result:
        flash('Salasanasi oli väärin', 'error')
        return render_template('change_password.html')
    
    flash('Salasanasi on vaihdettu', 'success')
    return redirect('/user/profile/'+str(session['id']))

@app.route('/user/profile/avatar/remove', methods=['POST'])
def remove_avatar():
    user.avatar_remove(session['id'])
    return redirect('/user/profile/modify')

@app.route('/user/profile/update', methods= ['POST'])
def update_profile():
    if 'file' in request.files:
        file = request.files['file']
        user.avatar_save(session['id'], file)
    pitch = request.form['pitch']
    region = request.form['region']
    user.update(pitch, region, session['id'])
    return redirect('/user/profile/modify') 

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    result = user.handleRegister(username, password)
    if 'error' in result:
        flash('Käyttäjätunnus on jo käytössä', 'error')
        return redirect('/signin')
    flash('Käyttäjätunnus on luotu, kirjaudu nyt sisään', 'success')
    return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'recentUrl' in request.form:
        session['url'] = request.form['recentUrl']
    return render_template('login.html')

@app.route('/login/check', methods=['POST'])
def checklogin():
    username = request.form['username']
    password = request.form['password']
    userQuery = user.handleLogin(username, password)

    if userQuery:
        session['username'] = userQuery[1]
        session['id'] = userQuery[0]
        flash('Tervetuloa, '+str(session['username']), 'success')
        if 'url' in session:
            url = session['url']
            del session['url']
            return redirect(url)
        return redirect('/')
    flash('Käyttäjä ja/tai salasana väärin', 'error')
    return redirect('/login')

@app.route('/logout')
def logout():
    del session['username']
    del session['id']
    flash('Olet kirjautunut ulos, nähdään taas pian :)', 'success')
    return redirect('/')

########################################################
### handle uploading

@app.route('/')
def index():
    advertisements = query.get_all()
    ## part query to 5 item pages
    current_page = request.args.get('page', 1, type=int)
    items_per_page = 5
    pages = round(len(advertisements)/items_per_page+ .499)
    from_page = int(current_page) * items_per_page - items_per_page
    upto_page = int(current_page) * items_per_page
    list_part = advertisements[from_page:upto_page]

    images = []
    for adv in list_part:
        images.append(query.get_images(adv[0]))

    return render_template('index.html', images=images, advertisements=list_part, pages=pages, current_page=current_page)

@app.route('/search', methods=['GET'])
def search():
    region= request.args['region']
    max=request.args['max']
    min=request.args['min']
    result= query.search(region, min, max)
    current_page = request.args.get('page', 1, type=int)
    items_per_page = 5
    pages = round(len(result)/items_per_page+ .499)
    from_page = int(current_page) * items_per_page - items_per_page
    upto_page = int(current_page) * items_per_page
    list_part = result[from_page:upto_page]

    images = []
    for adv in list_part:
        images.append(query.get_images(adv[0]))

    return render_template('search.html', images=images, advertisements=list_part, pages=pages, current_page=current_page, region=region, max=max, min=min)

#####################################################################################################################################
@app.route('/advertisement/publish', methods=['POST'])
def publish():
    advert_id = request.form['advert_id']
    query.publish(advert_id, session['id'])
    flash('Ilmoituksesi on julkaistu', 'success')
    return redirect('/advertisement/show/'+str(advert_id))

@app.route('/advertisement/unpublished')
def show_unpub_adv():
    incompletes = query.get_incompletes(session['id'])
    images = []
    for incomplete in incompletes:
        advert_id = incomplete[0]
        result = query.get_images(advert_id)
        images.append(result)
    print(images)
    return render_template('create.html', advertisements=incompletes, images=images)

@app.route('/advertisement/new', methods=['POST'])
def new_adv():
    advertisement_id = query.new(session['id'])
    return redirect('/advertisement/edit/'+str(advertisement_id))

@app.route('/advertisement/edit/<int:id>', methods=['GET'])
def edit_adv(id):
    images = query.get_images(id)
    advertisement = query.get(id)
    if advertisement:
        if advertisement[1]!=session['id']:
            return page_not_found
    return render_template('edit.html', images=images,advertisement=advertisement, advertisement_id=id)

@app.route('/advertisement/delete', methods=['POST'])
def delete_adv():
    id=request.form['id']
    query.remove(id, session['id'])
    flash('Ilmoituksesi on poistettu', 'success')
    return redirect('/')

@app.route('/advertisement/image/delete', methods=['POST'])
def adv_delete_image():
    image_id=request.form['img-id']
    query.image_remove(image_id) 
    adv_id=request.form['advertisement_id']
    flash('Kuva poistettu', 'success')
    return redirect('/advertisement/edit/'+str(adv_id))

@app.route('/advertisement/update', methods=['POST'])
def update_adv():
    id = request.form['id']
    content = request.form['content']
    header = request.form['header']
    price = request.form['price']
    region = request.form.get('region')

    if 'file' in request.files:
        file=request.files['file']
        query.image_save(id, file)

    query.update(content, header, price, id, region)
    flash('Tiedot tallennettu', 'success')
    return redirect('/advertisement/edit/'+str(id))

@app.route('/advertisement/show/<int:id>')
def show_adv(id):
    advertisement = query.get(id)
    if 'error' in advertisement:
        page_not_found('Wrong id')
    images = query.get_images(id)
    return render_template('advertisement.html', advertisement=advertisement, images=images)

@app.route('/show/image/<int:id>')
def show_img(id):
    data = query.image_show(id)
    response = make_response(bytes(data))
    response.headers.set('Content-Type', 'image/jpeg')
    return response
