DROP TABLE IF EXISTS grupo;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS site;
DROP TABLE IF EXISTS sensor;
DROP TABLE IF EXISTS alert;
DROP TABLE IF EXISTS invernadero1;

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
INSERT INTO user(username,password,grupo_id) 
        VALUES('admin','pbkdf2:sha256:50000$6HukpQzY$f158ecf781ecaa3aaf29d398add8864a51f10bf0fd3d0e6ec4b68081156606b3',1); 

CREATE TABLE site (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL
);
INSERT INTO site(name,description) VALUES('invernadero1','Invernadero 1');
INSERT INTO site(name,description) VALUES('invernadero2','Invernadero 2');


CREATE TABLE sensor (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  site_id INTEGER NOT NULL,
  datatype TEXT NOT NULL,
  unit TEXT NOT NULL,
  min real NOT NULL,
  max real NOT NULL,
  FOREIGN KEY (site_id) REFERENCES site (id),
  CHECK ( datatype IN ('integer','real','datetime'))
);
INSERT INTO sensor(name,site_id,datatype,unit,min,max) VALUES('cTemp',1,'real','&deg;C',0,45);
INSERT INTO sensor(name,site_id,datatype,unit,min,max) VALUES('humidity',1,'real','%',0,100);
INSERT INTO sensor(name,site_id,datatype,unit,min,max) VALUES('cTemp',2,'real','&deg;C',0,45);
INSERT INTO sensor(name,site_id,datatype,unit,min,max) VALUES('humedad',2,'real','%',0,100);

CREATE TABLE actuator (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  status INTEGER NOT NULL,
  sensor_id  INTEGER NOT NULL,
  FOREIGN KEY (sensor_id) REFERENCES sensor (id),
  CHECK ( status IN (0,1))

);
INSERT INTO actuator(name,status,sensor_id) VALUES('aspersor',1,1);
INSERT INTO actuator(name,status,sensor_id) VALUES('ventilador',0,1);
INSERT INTO actuator(name,status,sensor_id) VALUES('electroValvula',0,1);
INSERT INTO actuator(name,status,sensor_id) VALUES('electroValvula2',0,2);



CREATE TABLE alert (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);


CREATE TABLE sitetableinvernadero1 (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date datetime, 
  cTemp real, 
  humidity real
);
INSERT INTO sitetableinvernadero1(date,cTemp,humidity) VALUES('20190405115900','23.9','50.0');
INSERT INTO sitetableinvernadero1(date,cTemp,humidity) VALUES('20190405115910','24.9','60.0');
INSERT INTO sitetableinvernadero1(date,cTemp,humidity) VALUES('20190405115920','25.9','70.0');
INSERT INTO sitetableinvernadero1(date,cTemp,humidity) VALUES('20190405115930','23.9','65.0');
INSERT INTO sitetableinvernadero1(date,cTemp,humidity) VALUES('20190405115940','22.9','50.0');
INSERT INTO sitetableinvernadero1(date,cTemp,humidity) VALUES('20190405115950','21.9','48.0');
INSERT INTO sitetableinvernadero1(date,cTemp,humidity) VALUES('20190406120130','24','42.1');
INSERT INTO sitetableinvernadero1(date,cTemp,humidity) VALUES('20190406120230','22','40.1');
INSERT INTO sitetableinvernadero1(date,cTemp,humidity) VALUES('20190406120250','23','41.1');
INSERT INTO sitetableinvernadero1(date,cTemp,humidity) VALUES('20190406120350','19','60.1');



CREATE TABLE sitetableinvernadero2  ( 
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  date datetime , 
  cTemp real, 
  humedad real
);

INSERT INTO sitetableinvernadero2(date,cTemp,humedad) VALUES('20190406115900','20.9','40.0');
INSERT INTO sitetableinvernadero2(date,cTemp,humedad) VALUES('20190406120000','21.9','41.0');
INSERT INTO sitetableinvernadero2(date,cTemp,humedad) VALUES('20190406120020','22','41.1');
INSERT INTO sitetableinvernadero2(date,cTemp,humedad) VALUES('20190406120030','22.3','42.1');
INSERT INTO sitetableinvernadero2(date,cTemp,humedad) VALUES('20190406120110','24.3','43.1');
INSERT INTO sitetableinvernadero2(date,cTemp,humedad) VALUES('20190406120130','24','42.1');
INSERT INTO sitetableinvernadero2(date,cTemp,humedad) VALUES('20190406120230','22','40.1');
INSERT INTO sitetableinvernadero2(date,cTemp,humedad) VALUES('20190406120250','23','41.1');
INSERT INTO sitetableinvernadero2(date,cTemp,humedad) VALUES('20190406120350','19','60.1');

