from db import db



def chat_getmessages(chat_id, user_id):
    ## check if participant in chat
    sql = "SELECT c.id FROM chat as c JOIN participant as p ON p.participant_id=:p_id AND c.id=:chat_id"
    chat_ids = db.session.execute(sql, {"p_id":user_id, "chat_id":chat_id}).fetchone()
    if chat_ids:
        sql = "SELECT * FROM message WHERE chat_id=:chat_id"
        result = db.session.execute(sql, {"chat_id":chat_ids[0]}).fetchall()
        return result

    return "permission denied"

def chat_active(creator_id, advertisement_id):
    sql = "SELECT c.id FROM chat as c JOIN participant as p ON p.participant_id=:p_id AND c.advertisement_id=:advertisement_id"
    chat_id = db.session.execute(sql, {"p_id":creator_id, "advertisement_id":advertisement_id}).fetchone()
    return chat_id

def chat_get_all(participant_id):
    sql = "SELECT c.id, c.advertisement_id, u.username FROM chat as c JOIN participant as p ON p.participant_id=:p_id  JOIN users as u ON u.id=:p_id"
    result = db.session.execute(sql,{"p_id":participant_id})
    return result.fetchall()

def chat_create(creator_id, advertisement_id, content):
    # create chat db
    sql = "INSERT INTO chat (advertisement_id) VALUES (:advertisement_id) RETURNING id"
    chat_id = db.session.execute(sql, {"advertisement_id": advertisement_id}).fetchone()[0]

    # add participants to chat
    sql = "SELECT user_id FROM advertisement WHERE id=:advertisement_id"
    adv_owner = db.session.execute(sql, {'advertisement_id':advertisement_id}).fetchone()[0]
    sql = "INSERT INTO participant (chat_id, participant_id) VALUES (:chat_id, :participant_id) "
    db.session.execute(sql, {'chat_id':chat_id, 'participant_id':creator_id})
    db.session.execute(sql, {'chat_id':chat_id, 'participant_id':adv_owner})
    db.session.commit()

    # send message
    sql = "INSERT INTO message (creator_id, chat_id, content) VALUES (:creator_id, :chat_id, :content)"
    db.session.execute(sql, {'creator_id':creator_id, 'chat_id':chat_id, 'content':content})
    db.session.commit()
    return chat_id

    
def chat_message_send(chat_id, message, creator_id):
    sql = "INSERT INTO message (creator_id, chat_id, content) VALUES (:creator_id, :chat_id, :content)"
    db.session.execute(sql, {"creator_id":creator_id, "chat_id":chat_id, "content":message})
    db.session.commit()
    return "OK"
