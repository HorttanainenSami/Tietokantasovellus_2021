CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT,
  password TEXT,
  created_at TIMESTAMP,
  info TEXT,
  region TEXT
);

CREATE TABLE advertisement (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users ON DELETE CASCADE,
  region TEXT,
  published BOOLEAN,
  published_at TIMESTAMP, 
  header TEXT,
  price INTEGER,
  content TEXT
);
CREATE TABLE images (
  id SERIAL PRIMARY KEY,
  advertisement_id INTEGER REFERENCES advertisement ON DELETE CASCADE,
  name TEXT,
  data BYTEA,
  avatar BOOLEAN,
  user_id INTEGER REFERENCES users ON DELETE CASCADE
);
CREATE TABLE chat (
  id SERIAL PRIMARY KEY,
  advertisement_id INTEGER REFERENCES advertisement ON DELETE CASCADE
);
CREATE TABLE participant (
  chat_id INTEGER REFERENCES chat ON DELETE CASCADE, 
  participant_id INTEGER REFERENCES users ON DELETE CASCADE
);
CREATE TABLE message (
  id SERIAL PRIMARY KEY,
  creator_id INTEGER REFERENCES users ON DELETE CASCADE,
  chat_id INTEGER REFERENCES chat ON DELETE CASCADE,
  content TEXT,
  created_at TIMESTAMP
);
