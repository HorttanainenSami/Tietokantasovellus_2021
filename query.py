from db import db 

def search(region, min, max):
    sql  = 'SELECT id, published_at, header, price, content FROM advertisement WHERE published=true AND region=:region AND price BETWEEN :min AND :max ORDER BY published_at'
    result = db.session.execute(sql, {'region':region, 'min':min, 'max':max})
    return result.fetchall()

def get_adverts():
    sql  = 'SELECT id, published_at, header, price, content FROM advertisement WHERE published=true ORDER BY published_at'
    result = db.session.execute(sql)
    return result.fetchall()

def advert_update(content, header,price, id, region):
    sql = "UPDATE advertisement SET region=:region, content=:content, header=:header, price=:price WHERE id =:id"
    db.session.execute(sql,{'region':region,"id":id, "content":content, "header":header,"price":price})
    db.session.commit()

def advert_new(id):
    sql = "INSERT INTO advertisement (user_id,region, published, header, content,price) VALUES (:user_id, NULL, FALSE, '', '', 0) RETURNING id"
    advertisement_id = db.session.execute(sql, {"user_id":id})
    db.session.commit()
    return advertisement_id.fetchone()[0]

def get_published(user_id):
    sql ='SELECT id, published_at, header, price, content FROM advertisement as a WHERE a.published=TRUE AND a.user_id=:user_id ORDER BY a.published_at' 
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_incomplete(user_id, advertisement_id):
    sql = "SELECT id, published_at, header, price, content FROM advertisement WHERE user_id=:user_id AND id=:id"
    result = db.session.execute(sql, {"user_id":user_id, "id":advertisement_id})
    return result.fetchone()

def get_incompletes(user_id):
    sql = "SELECT id, published_at, header, price, content FROM advertisement WHERE published=FALSE AND user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall() 

def get_advert(id):
    sql = "SELECT a.id, u.id, a.header, a.price, a.content, a.published_at, u.username, i.id, a.region from advertisement as a LEFT JOIN users as u ON u.id=a.user_id LEFT JOIN images as i ON i.user_id=u.id WHERE a.id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    if result == None:
        return 'Wrong id'
    return result

def advert_remove(id,user_id):
    ## delete chats also and messages
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
    sql = "SELECT * FROM images WHERE advertisement_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def image_show(id):
    sql = "SELECT data FROM images WHERE id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    if result == None:
        return 'Wrong id'
    return result[0]

def image_remove(img_id):
    sql='DELETE FROM images as i WHERE i.id=:img_id'
    db.session.execute(sql, { 'img_id':img_id})
    db.session.commit()
    return

def image_save(id, file):
    name = file.filename
    if not name.endswith(".jpeg"):
        print("invalid filename")
        return "Invalid filename"
    data = file.read()
    if len(data) > 100*1024:
        print("too big")
        return "Too big file"
    sql = "INSERT INTO images (data, advertisement_id) VALUES (:data, :advertisement_id)"
    db.session.execute(sql, {"data":data, "advertisement_id":id})
    db.session.commit()
    return "OK"
