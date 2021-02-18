from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username}) 
    user = result.fetchone()

    if user == None:
        # wrong password or username 
        return(None)
    else:
        #correct username
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            # correct username and password, login
            return(username)
        
    #incorrect password
    return(None)

## KYSY onko tämä turvallinen tapa siirtää salasana, vai pitääkö se siirtää jo salattuna
def register(username, password):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password" : hash_value})
    db.session.commit() 
    return()

def id(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    id= result.fetchone()[0]
    print(id)
    return id 
