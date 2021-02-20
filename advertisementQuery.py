from db import db 

def sendimage(id, file):
    name = file.filename
    if not name.endswith(".jpeg"):
        print("invalid filename")
        return "Invalid filename"
    data = file.read()
    if len(data) > 100*1024:
        print("too big")
        return "Too big file"
    sql = "INSERT INTO images (name, data, advertisement_id) VALUES (:name, :data, :advertisement_id)"
    db.session.execute(sql, {"name":name,"data":data, "advertisement_id":id})
    db.session.commit()
    return "OK"

def updateContent(content, header, id):
    print(header)
    sql = "UPDATE advertisement SET content=:content, header=:header WHERE id =:id"
    db.session.execute(sql,{"id":id, "content":content, "header":header})
    db.session.commit()

def newAdvertisement(id):
    sql = "INSERT INTO advertisement (user_id,localaddress_id, published, header, content) VALUES (:user_id, NULL, FALSE, '', '') RETURNING id"
    advertisement_id = db.session.execute(sql, {"user_id":id})
    db.session.commit()
    return advertisement_id.fetchone()[0]

def getIncomplete(user_id, advertisement_id):
    sql = "SELECT * FROM advertisement WHERE user_id=:user_id AND id=:id"
    result = db.session.execute(sql, {"user_id":user_id, "id":advertisement_id})
    return result.fetchone()

def getIncompletes(user_id):
    sql = "SELECT * FROM advertisement WHERE published=FALSE AND user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall() 

def fetchImages(id):
    sql = "SELECT id FROM images WHERE advertisement_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def show(id):
    sql = "SELECT data FROM images WHERE id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    if result == None:
        return 'Wrong id'
    return result[0]

def removeAdvertisement(id):
    sql = "DELETE FROM advertisement WHERE id=:id"
    db.session.execute(sql, {"id":id})
    sql = "DELETE FROM images WHERE advertisement_id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return "OK"
