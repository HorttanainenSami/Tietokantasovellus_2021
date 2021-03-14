from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def handleLogin(username, password):
    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username}) 
    user = result.fetchone()

    if user == None:
        # wrong username 
        return(None)
    else:
        #correct username
        correct_hash_value= user[2]
        if check_password_hash(correct_hash_value, password):
            # correct username and password, login
            return(user)
        
    #incorrect password
    return(None)

def handleRegister(username, password):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password, created_at) VALUES (:username, :password, NOW())"
    db.session.execute(sql, {"username":username, "password" : hash_value})
    db.session.commit() 
    return()
