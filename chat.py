from db import db



def chat_getmessages(chat_id, user_id):
    ## check if participant in chat
    sql = 'SELECT * from participant WHERE chat_id =:chat_id AND participant_id =:p_id'
    result = db.session.execute(sql, {"p_id":user_id, "chat_id":chat_id}).fetchone()
    if result:
        sql = "SELECT * FROM message WHERE chat_id=:chat_id"
        result = db.session.execute(sql, {"chat_id":chat_id}).fetchall()
        return result

    return "permission denied"

def chat_active(creator_id, advertisement_id):
    sql = 'SELECT * FROM chat as c WHERE advertisement_id=:advertisement_id AND (SELECT p.chat_id FROM participant as p WHERE c.id=p.chat_id AND p.participant_id=:p_id) IS NOT NULL'
    chat_id = db.session.execute(sql, {"p_id":creator_id, "advertisement_id":advertisement_id}).fetchone()
    return chat_id

def chat_get_all(participant_id):
    sql = 'SELECT p.chat_id, c.advertisement_id, (SELECT u.username from users as u, participant as p1 WHERE u.id=p1.participant_id AND p1.chat_id=p.chat_id AND p1.participant_id!=:participant_id ) FROM participant as p , chat as c WHERE c.id = p.chat_id AND p.participant_id=:participant_id'
    result = db.session.execute(sql, {"participant_id":participant_id})
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
    chat_message_send(chat_id, content, creator_id)
    return chat_id

    
def chat_message_send(chat_id, message, creator_id):
    sql = "INSERT INTO message (creator_id, chat_id, content) VALUES (:creator_id, :chat_id, :content)"
    db.session.execute(sql, {"creator_id":creator_id, "chat_id":chat_id, "content":message})
    db.session.commit()
    return "OK"
