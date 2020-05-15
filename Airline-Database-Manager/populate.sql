CREATE TABLE passenger(
	cnic		INT				NOT NULL,
	full_name	VARCHAR (40)	NOT NULL,
	nationality	VARCHAR (40)	NOT NULL,
	address		VARCHAR (40),
	phone		INT,
	PRIMARY KEY (cnic)
);

CREATE TABLE flight(
	flight_id 			VARCHAR (6)	NOT NULL,
	flight_date			DATE		NOT NULL,
	departure_time		TIME		NOT NULL,
	arrival_time		TIME		NOT NULL,
	departure_airport	CHAR (3)	NOT NULL,
	arrival_airport		CHAR (3)	NOT NULL,
	fare				INT			NOT NULL,
	airplane			VARCHAR (8)	NOT NULL,
	PRIMARY KEY (flight_id)
);

CREATE TABLE ticket(
	cnic				INT			NOT NULL,
	flight_id 			VARCHAR (6)	NOT NULL,
	FOREIGN KEY (cnic) references passenger (cnic),
	FOREIGN KEY (flight_id) references flight (flight_id)
);





INSERT INTO flight VALUES ("PK303", "12-12-10", "20:00", "23:00", "LHE", "DHL", 5000, "BOE-888");
INSERT INTO flight VALUES ("PK304", "13-01-10", "20:00:00", "23:00:00", "LHE", "DHL", 8000, "BOE-888");
INSERT INTO flight VALUES ("PK305", "13-01-11", "18:00", "23:00", "LHE", "DHL", 1000, "BOE-777");
INSERT INTO flight VALUES ("PK306", "13-01-12", "20:00", "23:00", "LHE", "DHL", 5000, "BOE-888");
INSERT INTO flight VALUES ("PK307", "20-03-13", "20:00", "23:00", "LHE", "DHL", 6000, "BOE-777");
INSERT INTO flight VALUES ("KLM200", "20-03-13", "5:00", "13:00", "LHE", "AMS", 60000, "BOE-555");
INSERT INTO flight VALUES ("QT200", "20-03-13", "12:00", "16:00", "DOH", "LHE", 10000, "BOE-565");
INSERT INTO flight VALUES ("QT199", "20-03-13", "09:00", "11:00", "LHE", "DOH", 11000, "BOE-865");
INSERT INTO flight VALUES ("QT201", "20-04-13", "12:00", "16:00", "DOH", "LHE", 90000, "BOE-865");
INSERT INTO flight VALUES ("KLM201", "20-03-20", "5:00", "13:00", "LHE", "AMS", 45000, "BOE-505");
INSERT INTO flight VALUES ("KLM202", "20-03-27", "5:00", "13:00", "LHE", "AMS", 60000, "BOE-605");
INSERT INTO flight VALUES ("KLM377", "20-11-05", "5:00", "13:00", "LHE", "AMS", 40000, "BOE-805");
INSERT INTO flight VALUES ("KLM390", "20-10-30", "5:00", "13:00", "LHE", "AMS", 55000, "BOE-805");


INSERT INTO ticket VALUES (563, "PK303");
INSERT INTO ticket VALUES (808, "PK303");
INSERT INTO ticket VALUES (550, "PK303");
INSERT INTO ticket VALUES (202, "PK303");
INSERT INTO ticket VALUES (606, "PK303");
INSERT INTO ticket VALUES (606, "PK306");
INSERT INTO ticket VALUES (606, "PK304");
INSERT INTO ticket VALUES (550, "PK305");
INSERT INTO ticket VALUES (550, "PK306");
INSERT INTO ticket VALUES (550, "PK307");
INSERT INTO ticket VALUES (550, "KLM202");
INSERT INTO ticket VALUES (550, "KLM390");


INSERT INTO passenger VALUES (350, "abc lol", "Wakanda", "91 Privet Drive LHR", 7777);
INSERT INTO passenger VALUES (808, "Shaitaan", "Saudi Arabia", "Underworld", 666);
INSERT INTO passenger VALUES (353, "abc xyz", "Wakanda", "91 Privet Drive LHR", 7777);
INSERT INTO passenger VALUES (563, "Lord Voldemort", "England", "Hogwarts", 934);
INSERT INTO passenger VALUES (550, "Harry Putter", "Great Britania", "Ron's House", 007);
INSERT INTO passenger VALUES (777, "Voldy's Mistress", "Wakanda", "91 Privet Drive LHR", 7777);
INSERT INTO passenger VALUES (123, "Donny Trumpet", "Muricaa", "WHITE HOUSE", 911);
INSERT INTO passenger VALUES (724, "Putin", "Russia", "Moscow's Gulags", 919228);
INSERT INTO passenger VALUES (202, "Nabeel H Rizv", "Paki Boi", "LUMZ University", 8371);
INSERT INTO passenger VALUES (606, "Donny Waffle", "Paki Boi", "house in Phase V", 91919);
INSERT INTO passenger VALUES (333, "Sadam Hussein", "Iraq", "Jannat", 303);
INSERT INTO passenger VALUES (452, "Malik Riaz", "Paki Boi", "Bahria Town HNO 1", 72777);
INSERT INTO passenger VALUES (229, "Faridoon", "Iran", "Lucky gardens", 35335);
INSERT INTO passenger VALUES (230, "Firdawsi", "Iran", "Lucky gardens (2)", 35336);



