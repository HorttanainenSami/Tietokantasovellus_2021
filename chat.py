from db import db
import datetime



def get_messages(chat_id, user_id):
    ## check if participant in chat
    sql = 'SELECT * FROM participant as p, message as m WHERE p.chat_id=:chat_id AND m.chat_id=p.chat_id AND p.participant_id=:p_id ORDER BY m.created_at'
    result = db.session.execute(sql, {"p_id":user_id, "chat_id":chat_id}).fetchall()
    return result

def get_active(creator_id, advertisement_id):
    sql = 'SELECT * FROM chat as c WHERE advertisement_id=:advertisement_id AND (SELECT p.chat_id FROM participant as p WHERE c.id=p.chat_id AND p.participant_id=:p_id) IS NOT NULL'
    chat_id = db.session.execute(sql, {"p_id":creator_id, "advertisement_id":advertisement_id}).fetchone()
    return chat_id
def get_participant(chat_id, user_id):
    ## fetch info of chat participant profile and what advertisement chat connects to
    sql = 'SELECT u.id, u.username, i.id, c.advertisement_id FROM chat as c, participant as p JOIN users as u ON u.id=p.participant_id LEFT JOIN images as i ON i.avatar=TRUE AND i.user_id=u.id WHERE p.chat_id=:chat_id AND p.participant_id!=:user_id AND c.id=p.chat_id'
    result = db.session.execute(sql, {'chat_id':chat_id, 'user_id':user_id})
    return result.fetchone()

def get_all(participant_id):
    ## valitsee kaikki viimeisimmäksi lähetetyt viestit,mikä chat, kenen lähettämä, milloin, mitä sisältää ja kuinka monta lukematonta viestiä sinulla on kyseisessä chatissa 
    sql = 'SELECT x.chat_id, u.username, u.id, x.content, x.created_at, x.unread, x.creator_id, i.id FROM participant as p,participant as p1, users as u LEFT JOIN images as i ON i.user_id=u.id, (SELECT COUNT(CASE WHEN creator_id=:p_id THEN NULL ELSE CASE WHEN is_read=FALSE THEN TRUE ELSE NULL END END) OVER(PARTITION BY chat_id) as unread, ROW_NUMBER() OVER (PARTITION BY chat_id ORDER BY created_at DESC) as rownum, * FROM message) X WHERE rownum=1 AND p.chat_id=x.chat_id AND p.participant_id=:p_id AND p1.chat_id=p.chat_id AND p1.participant_id!=p.participant_id AND u.id=p1.participant_id ORDER BY x.created_at DESC'
    result = db.session.execute(sql, {"p_id":participant_id})
    return result.fetchall()
    
def create(creator_id, advertisement_id, content):
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
    message_send(chat_id, content, creator_id)
    return chat_id

    
def message_send(chat_id, message, creator_id):
    sql = "INSERT INTO message (creator_id, chat_id, content, created_at, is_read) VALUES (:creator_id, :chat_id, :content, NOW(), FALSE)"
    db.session.execute(sql, {"creator_id":creator_id, "chat_id":chat_id, "content":message})
    db.session.commit()
    return "OK"
