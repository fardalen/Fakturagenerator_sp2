DROP DATABASE Innloggingsinformasjon;
CREATE DATABASE IF NOT EXISTS Innloggingsinformasjon; 

USE Innloggingsinformasjon;

CREATE TABLE IF NOT EXISTS TILSETTINFO(
TilsettID INT NOT NULL,
Fornamn VARCHAR(25) NOT NULL,
Etternamn VARCHAR(25) NOT NULL,
PRIMARY KEY (TilsettID)
);

CREATE TABLE IF NOT EXISTS innloggingsinfo(
BrukerID INT NOT NULL AUTO_INCREMENT,
TILSETTINFO_TilsettID INT NOT NULL,
Epost VARCHAR(50) NOT NULL,
Passord VARCHAR(200) NOT NULL, 
PRIMARY KEY (BrukerID),
FOREIGN KEY (TILSETTINFO_TilsettID) REFERENCES TILSETTINFO(TilsettID)
);






DROP DATABASE Faktura;

CREATE DATABASE IF NOT EXISTS Faktura;

USE Faktura;

CREATE TABLE IF NOT EXISTS TJENESTE(
ID INT NOT NULL AUTO_INCREMENT,
Namn VARCHAR(40) NOT NULL,
Pris INT NOT NULL,

PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS MATRIAL(
ID INT NOT NULL AUTO_INCREMENT,
Namn VARCHAR(40) NOT NULL,
Pris INT NOT NULL,

PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS POSTNR(
Postkode VARCHAR(4) NOT NULL,
by_namn VARCHAR(30) NOT NULL,
PRIMARY KEY(Postkode)
);

CREATE TABLE IF NOT EXISTS KUNDE(
ID INT NOT NULL AUTO_INCREMENT,
Namn VARCHAR(40) NOT NULL,
Epost VARCHAR(50) NOT NULL,
Adresse VARCHAR(40) NOT NULL,
POSTKODE_PostNR VARCHAR(4) NOT NULL,

PRIMARY KEY (ID),
FOREIGN KEY (POSTKODE_PostNR) REFERENCES POSTNR(Postkode) 
);

CREATE TABLE IF NOT EXISTS SELJAR(
ID INT NOT NULL,
Namn VARCHAR(20) NOT NULL,
Epost VARCHAR(50) NOT NULL,
Adresse VARCHAR(40) NOT NULL,
kontonummer VARCHAR(15) NOT NULL,
organisjonnr VARCHAR(9) NOT NULL,
POSTKODE_PostNR VARCHAR(4) NOT NULL,

PRIMARY KEY (ID),
FOREIGN KEY (POSTKODE_PostNR) REFERENCES POSTNR(Postkode)
);

CREATE TABLE IF NOT EXISTS TILSETTINFO(
TilsettID INT NOT NULL,
Fornamn VARCHAR(25) NOT NULL,
Etternamn VARCHAR(25) NOT NULL,

PRIMARY KEY (TilsettID)
);

CREATE TABLE IF NOT EXISTS JOBB(
ID INT NOT NULL AUTO_INCREMENT,
Timer_brukt INT NOT NULL,
TILSETTINFO_TilsettID INT NOT NULL,
MATRIAL_ID INT NOT NULL,
TJENESTE_ID INT NOT NULL,
Dato DATE NOT NULL,

PRIMARY KEY (ID),
FOREIGN KEY (TJENESTE_ID) REFERENCES TJENESTE(ID),
FOREIGN KEY (MATRIAL_ID) REFERENCES MATRIAL(ID),
FOREIGN KEY (TILSETTINFO_TilsettID) REFERENCES TILSETTINFO(TilsettID)
);

CREATE TABLE IF NOT EXISTS FAKTURA(
ID INT NOT NULL AUTO_INCREMENT,
KUNDE_ID INT NOT NULL,
SELJAR_ID INT NOT NULL,
JOBB_ID INT NOT NULL,
Dato_betaling DATE NOT NULL,
Total_pris INT NOT NULL,

PRIMARY KEY (ID),
FOREIGN KEY (JOBB_ID) REFERENCES JOBB(ID),
FOREIGN KEY (KUNDE_ID) REFERENCES KUNDE(ID),
FOREIGN KEY (SELJAR_ID) REFERENCES SELJAR(ID)

);

USE Innloggingsinformasjon;

INSERT INTO TILSETTINFO (TilsettID, Fornamn, Etternamn)
VALUES (1528, "Per","Hansen"),
(1689, "Kari", "Pettersen"),
(1523, "Tord", "Olsen"),
(1287, "Ola", "Nordmann"),
(1567, "Bent", "Dal"),
(1968, "Heidi", "Bakke"),
(1453, "Pål", "Strand"),
(1232, "Karl", "Karlsen");

USE Faktura;
INSERT INTO Matrial (ID, Namn, Pris)
VALUES (1, "Liten nettverks pakke", 35000),
(2, "middels nettverks pakke", 50000),
(3, "Stor nettverks pakke", 75000),
(4, "Betjeningsanlegg", 35000),
(5, "Ingen", 0);

INSERT INTO POSTNR (Postkode, by_namn)
VALUES ("0252", "Oslo");

INSERT INTO SELJAR(ID, Namn, Epost, Adresse, kontonummer, organisjonnr, POSTKODE_PostNR)
VALUES (1, "CounsultAS","sales@consult.no", "Tjuvholmen allé 3", "1111 22 33334", "98765432", "0252"); 


INSERT INTO TJENESTE (ID, Namn, Pris)
VALUES (1, "Implentasjon liten nettverksarkitektur", 350),
(2, "Implentasjon middels nettverksarkitektur", 700),
(3, "Implentasjon stor nettverksarkitektur", 1050), 
(4, "Alarm og signalanlegg", 380);

SELJAR_ID, JOBB_ID, Dato_betaling, Total_pris

SELECT jobb.Timer_brukt, jobb.dato, TJENESTE.Namn, TJENESTE.Pris, MATRIAL.namn, MATRIAL.pris
FROM FAKTURA
INNER JOIN jobb ON FAKTURA.Jobb_ID = jobb.ID
INNER JOIN TJENESTE ON JOBB.TJENESTE_ID = TJENESTE.ID
INNER JOIN MATRIAL ON JOBB.MATRIAL_ID = MATRIAL.ID
WHERE FAKTURA.ID = 1
GROUP BY FAKTURA.ID;

SELECT kunde.namn, kunde.Epost, kunde.Adresse, POSTKODE_PostNR, POSTNR.by_namn
FROM faktura
INNER JOIN kunde ON FAKTURA.KUNDE_ID = KUNDE.ID
INNER JOIN POSTNR ON KUNDE.POSTKODE_PostNR = POSTNR.Postkode
WHERE FAKTURA.ID = 1
GROUP BY FAKTURA.ID;

SELECT SELJAR.namn, SELJAR.Adresse, SELJAR.kontonummer, POSTKODE_PostNR, POSTNR.by_namn
FROM faktura
INNER JOIN SELJAR ON FAKTURA.SELJAR_ID = SELJAR.ID
INNER JOIN POSTNR ON SELJAR.POSTKODE_PostNR = POSTNR.Postkode
WHERE FAKTURA.ID = 1
GROUP BY FAKTURA.ID;