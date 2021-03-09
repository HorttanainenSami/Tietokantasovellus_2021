CREATE TABLE postaladdress (
  id SERIAL PRIMARY KEY,
  postcode TEXT,
  post_office TEXT
);

CREATE TABLE localaddress (
  id SERIAL PRIMARY KEY,
  address TEXT,
  postaladdress_id INTEGER REFERENCES postaladdress
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT,
  password TEXT,
  created_at TIMESTAMP
);

CREATE TABLE advertisement (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users ON DELETE CASCADE,
  localAddress_id INTEGER REFERENCES localaddress,
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
  creator_id INTEGER REFERENCES participant ON DELETE CASCADE,
  chat_id INTEGER REFERENCES chat,
  content TEXT
);
