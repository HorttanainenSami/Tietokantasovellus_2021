from db import db 

def get_adverts():
    sql  = "SELECT * FROM advertisement"
    result = db.session.execute(sql)
    return result.fetchall()

def advert_update(content, header,price, id):
    sql = "UPDATE advertisement SET content=:content, header=:header, price=:price WHERE id =:id"
    db.session.execute(sql,{"id":id, "content":content, "header":header,"price":price})
    db.session.commit()

def advert_new(id):
    sql = "INSERT INTO advertisement (user_id,localaddress_id, published, header, content,price) VALUES (:user_id, NULL, FALSE, '', '', '') RETURNING id"
    advertisement_id = db.session.execute(sql, {"user_id":id})
    db.session.commit()
    return advertisement_id.fetchone()[0]

def get_advert_published(user_id):
    sql = "SELECT * FROM advertisement WHERE published=TRUE AND user_id=:user_id" 
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_advert_incomplete(user_id, advertisement_id):
    sql = "SELECT * FROM advertisement WHERE user_id=:user_id AND id=:id"
    result = db.session.execute(sql, {"user_id":user_id, "id":advertisement_id})
    return result.fetchone()

def get_advert_incompletes(user_id):
    sql = "SELECT * FROM advertisement WHERE published=FALSE AND user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall() 

def get_advert(id):
    sql = "SELECT * from advertisement WHERE id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    if result == None:
        return 'Wrong id'
    return result

def advert_remove(id,user_id):
    sql = "SELECT id FROM advertisement WHERE id=:id AND user_id=:user_id"
    result = db.session.execute(sql, {"id":id, "user_id":user_id})
    if result:
        sql = "DELETE FROM images WHERE advertisement_id=:id"
        db.session.execute(sql, {"id":id})
    sql = "DELETE FROM advertisement WHERE id=:id AND user_id=:user_id"
    db.session.execute(sql, {"id":id, "user_id":user_id})
    db.session.commit()
    return "OK"

def advert_publish(id, user_id):
    sql = "UPDATE advertisement SET published=TRUE, published_at =NOW() WHERE id=:id AND user_id=:user_id"
    db.session.execute(sql, {"id":id, "user_id":user_id})
    db.session.commit()
    return "OK"

def get_images(id):
    sql = "SELECT id FROM images WHERE advertisement_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def image_show(id):
    sql = "SELECT data FROM images WHERE id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    if result == None:
        return 'Wrong id'
    return result[0]

def image_save(id, file):
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
