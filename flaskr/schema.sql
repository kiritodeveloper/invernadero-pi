DROP TABLE IF EXISTS grupo;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS sensors;
DROP TABLE IF EXISTS alerts;

CREATE TABLE grupo (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL
);
INSERT INTO grupo(name,description) VALUES('admin','Administrador de todo');

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  grupo_id INTEGER NOT NULL,
  FOREIGN KEY (grupo_id) REFERENCES grupo (id)
);
INSERT INTO user(username,password,grupo_id) VALUES('admin','admin',1); 

CREATE TABLE places (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL
);
INSERT INTO places(name,description) VALUES('invernadero01','Invernadero 1');


CREATE TABLE sensors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  place_id INTEGER NOT NULL,
  FOREIGN KEY (place_id) REFERENCES places (id)
);
INSERT INTO sensors(name,place_id) VALUES('temperatura',1);
INSERT INTO sensors(name,place_id) VALUES('humedad',1);

CREATE TABLE alerts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);


CREATE TABLE invernadero1 (
  date datetime, 
  cTemp real, 
  humidity real
);
INSERT INTO invernadero1 VALUES('20190405115900','23.9','50.0');
INSERT INTO invernadero1 VALUES('20190405115910','24.9','60.0');
INSERT INTO invernadero1 VALUES('20190405115920','25.9','70.0');
INSERT INTO invernadero1 VALUES('20190405115930','23.9','65.0');
INSERT INTO invernadero1 VALUES('20190405115940','22.9','50.0');
INSERT INTO invernadero1 VALUES('20190405115950','21.9','48.0');

