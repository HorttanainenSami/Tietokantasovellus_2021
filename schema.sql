CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT,
  password TEXT,
  created_at TIMESTAMP,
  avatar BYTEA,
  reside TEXT,
  info TEXT
);

CREATE TABLE advertisement (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users ON DELETE CASCADE,
  localAddress_id TEXT,
  published BOOLEAN,
  published_at TIMESTAMP, 
  header TEXT,
  price TEXT,
  content TEXT
);
CREATE TABLE images (
  id SERIAL PRIMARY KEY,
  advertisement_id INTEGER REFERENCES advertisement ON DELETE CASCADE,
  name TEXT,
  data BYTEA
);
CREATE TABLE chat (
  id SERIAL PRIMARY KEY,
  advertisement_id INTEGER REFERENCES advertisement
);
CREATE TABLE participant (
  chat_id INTEGER REFERENCES chat,
  participant_id INTEGER REFERENCES users
);
CREATE TABLE message (
  id SERIAL PRIMARY KEY,
  creator_id INTEGER REFERENCES users ON DELETE CASCADE,
  chat_id INTEGER REFERENCES chat,
  content TEXT,
  created_at TIMESTAMP,
  is_read BOOLEAN 
);
