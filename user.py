from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def handleLogin(username, password):
    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if user is None:
        # wrong username
        return None
    else:
        #correct username
        correct_hash_value= user[2]
        if check_password_hash(correct_hash_value, password):
            # correct username and password, login
            return user
    #incorrect password
    return None

def handleRegister(username, password):
    sql = 'SELECT * FROM users WHERE username=:username'
    result = db.session.execute(sql, {'username':username}).fetchone()
    if result is not None:
        return 'error'
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password, created_at) VALUES (:username, :password, NOW())"
    db.session.execute(sql, {"username":username, "password" : hash_value})
    db.session.commit()
    return()

def get_user(user_id):
    sql = 'SELECT u.id, u.username,u.created_at, reside, info, i.id, i.data FROM users as u LEFT join images as i ON i.user_id = u.id AND i.avatar=true WHERE u.id=:user_id'
    result = db.session.execute(sql, {'user_id':user_id})
    return result.fetchone()

def avatar_save(user_id, file):
    name = file.filename
    if not name.endswith(tuple(['.jpeg', '.png'])):
        return "Invalid filename"
    data = file.read()
    if len(data) > 100*1024:
        return "Too big file"
    sql = "INSERT INTO images (data,avatar, user_id) VALUES (:data, TRUE,:user_id)"
    db.session.execute(sql, {"data":data, "user_id":user_id})
    db.session.commit()
    return "OK"

def avatar_remove(user_id):
    sql = 'DELETE FROM images WHERE user_id=:user_id AND avatar=TRUE'
    db.session.execute(sql, {'user_id': user_id})
    db.session.commit()
    return 'OK'

def update(pitch, reside, user_id):
    sql = 'UPDATE users SET info=:pitch, reside=:reside  WHERE id=:user_id'
    db.session.execute(sql, {'pitch':pitch, 'reside':reside, 'user_id':user_id})
    db.session.commit()
    return 'OK'
    
def change_password(old, new, user_id):
    sql = 'SELECT password FROM users WHERE id=:id'
    correct_hash = db.session.execute(sql, {'id':user_id}).fetchone()

    if correct_hash is not None:
        if check_password_hash(correct_hash[0], old):
            print('toka')
            new_hash=generate_password_hash(new)
            sql = 'UPDATE users SET password=:new_hash WHERE id =:user_id'
            db.session.execute(sql, {'new_hash':new_hash, 'user_id':user_id})
            db.session.commit()
            return 'OK'
    return 'error'
def remove_user(user_id):
    sql= 'DELETE FROM users WHERE id=:user_id'
    db.session.execute(sql, {'user_id':user_id})
    db.session.commit()
    return 'OK'
