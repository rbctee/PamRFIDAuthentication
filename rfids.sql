DROP TABLE names;
DROP TABLE identifiers;

CREATE TABLE names (
	name text PRIMARY KEY
);

CREATE TABLE identifiers (
	rfid text PRIMARY KEY,
	name text,
	FOREIGN KEY(name) REFERENCES names(name)
);

INSERT INTO names (name) VALUES ("user");
INSERT INTO identifiers (rfid,name) VALUES ("11223344","user");
-- INSERT INTO identifiers (rfid,name) VALUES ("55667788","user");
