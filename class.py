import mysql.connector as mysql
from datetime import date, timedelta

def connect(db_name):
    try:
        return mysql.connect(
            host='localhost',
            user='root',
            password='1234',
            database=db_name)
    except:
        print('kunne ikkje kople til database')

class Lagrefaktura:

    def __int__(self, kunde_by, kunde_namn, kunde_epost, kunde_adresse, kunde_postnr, timer_brukt, ansattid, matrial,
                tjeneste):
        self.kunde_postnr = kunde_postnr
        self.kunde_namn = kunde_namn
        self.kunde_epost = kunde_epost
        self.kunde_by = kunde_by
        self.kunde_adress = kunde_adresse
        self.timer_brukt = timer_brukt
        self.ansattid = ansattid
        self.matrial = matrial
        self.tjeneste = tjeneste

    def ikkje_kunde_postnr(self):
        db = connect("faktura")
        cursor = db.cursor(prepared=True)

        dato = date.today()
        betalingsdato = dato + timedelta(days=21)
        seljar_ID = 1

        hente_mpris = "SELECT PRIS from MATRIAL WHERE ID = %s"
        cursor.execute(hente_mpris, (self.matrial,))
        pris_matrial = cursor.fetchone()

        pris_matrial = pris_matrial[0]
        hente_tpris = "SELECT PRIS from TJENESTE WHERE ID = %s"
        cursor.execute(hente_tpris, (self.tjeneste,))
        pris_tjeneste = cursor.fetchone()
        pris_tjeneste = pris_tjeneste[0]

        insert_postnr = "INSERT INTO POSTNR(Postkode, by_namn) VALUES (%s,%s)"
        cursor.execute(insert_postnr, (self.kunde_postnr, self.kunde_by,))
        db.commit()
        insert_kunde = "INSERT INTO KUNDE(Namn, Epost, Adresse, POSTKODE_PostNR) VALUES (%s,%s,%s,%s)"
        cursor.execute(insert_kunde, (self.kunde_namn, self.kunde_epost, self.kunde_adress, self.kunde_postnr,))
        db.commit()
        insert_jobb = "INSERT INTO JOBB(Timer_brukt, TILSETTINFO_TilsettID, MATRIAL_ID, TJENESTE_ID, Dato " \
                      "VALUES (%s,%s,%s,%s,%s"
        cursor.execute(insert_jobb, (self.timer_brukt, self.ansattid, self.matrial, self.tjeneste, dato,))
        db.commit()
        hente_jobb = "SELECT ID FROM JOBB ORDER BY ID DESC LIMIT 1"
        cursor.execute(hente_jobb)
        jobb_id = cursor.fetchone()
        jobb_id = jobb_id[0]
        hente_kunde = "SELECT ID FROM KUNDE ORDER BY ID DESC LIMIT 1"
        cursor.execute(hente_kunde)
        kunde_id = cursor.fetchone()
        kunde_id = kunde_id[0]
        totalpris = (int(pris_tjeneste) * int(self.timer_brukt)) + int(pris_matrial)

        insert_faktura = "INSERT INTO FAKTURA(KUNDE_ID, SELJAR_ID, JOBB_ID, Dato_betaling, Total_pris) " \
                         "VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(insert_faktura, (kunde_id, seljar_ID, jobb_id, betalingsdato, totalpris,))
        db.commit()

    def postnr_ikkje_kunde(self):
        db = connect("faktura")
        cursor = db.cursor(prepared=True)

        dato = date.today()
        betalingsdato = dato + timedelta(days=21)
        seljar_ID = 1

        hente_mpris = "SELECT PRIS from MATRIAL WHERE ID = %s"
        cursor.execute(hente_mpris, (self.matrial,))
        pris_matrial = cursor.fetchone()

        pris_matrial = pris_matrial[0]
        hente_tpris = "SELECT PRIS from TJENESTE WHERE ID = %s"
        cursor.execute(hente_tpris, (self.tjeneste,))
        pris_tjeneste = cursor.fetchone()
        pris_tjeneste = pris_tjeneste[0]

        cursor.execute("INSERT INTO KUNDE(Namn, Epost, Adresse, POSTKODE_PostNR) VALUES (%s,%s,%s,%s)",
                       (self.kunde_namn, self.kunde_epost, self.kunde_adress, self.kunde_postnr,))
        db.commit()
        cursor.execute("INSERT INTO JOBB(Timer_brukt, TILSETTINFO_TilsettID, MATRIAL_ID, TJENESTE_ID, Dato)"
                       "VALUES (%s,%s,%s,%s,%s)", (self.timer_brukt, self.ansattid, self.matrial, self.tjeneste, dato,))
        db.commit()

        cursor.execute("SELECT ID FROM JOBB ORDER BY ID DESC LIMIT 1")
        jobb_id = cursor.fetchone()
        jobb_id = jobb_id[0]
        cursor.execute("SELECT ID FROM KUNDE ORDER BY ID DESC LIMIT 1")
        kunde_id = cursor.fetchone()
        kunde_id = kunde_id[0]
        totalpris = (int(pris_tjeneste) * int(self.timer_brukt)) + int(pris_matrial)

        cursor.execute("INSERT INTO FAKTURA(KUNDE_ID, SELJAR_ID, JOBB_ID, Dato_betaling, Total_pris) "
                       "VALUES (%s,%s,%s,%s,%s)", (kunde_id, seljar_ID, jobb_id, betalingsdato, totalpris,))
        db.commit()

    def kunde_postnr(self):
        db = connect("faktura")
        cursor = db.cursor(prepared=True)

        dato = date.today()
        betalingsdato = dato + timedelta(days=21)
        seljar_ID = 1

        hente_mpris = "SELECT PRIS from MATRIAL WHERE ID = %s"
        cursor.execute(hente_mpris, (self.matrial,))
        pris_matrial = cursor.fetchone()

        pris_matrial = pris_matrial[0]
        hente_tpris = "SELECT PRIS from TJENESTE WHERE ID = %s"
        cursor.execute(hente_tpris, (self.tjeneste,))
        pris_tjeneste = cursor.fetchone()
        pris_tjeneste = pris_tjeneste[0]

        hente_kunde = "SELECT ID FROM KUNDE WHERE Namn = %s AND Adresse =%s AND POSTKODE_PostNR =%s"
        cursor.execute(hente_kunde, (self.kunde_namn, self.kunde_adress, self.kunde_postnr))
        kundeid = cursor.fetchone()
        kundeid = kundeid[0]

        insert_jobb = "INSERT INTO JOBB(Timer_brukt, TILSETTINFO_TilsettID, MATRIAL_ID, TJENESTE_ID, Dato) " \
                      "VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(insert_jobb, (self.timer_brukt, self.ansattid, self.matrial, self.tjeneste, dato,))
        db.commit()

        hente_jobb = "SELECT ID FROM JOBB ORDER BY ID DESC LIMIT 1"
        cursor.execute(hente_jobb)
        jobb_id = cursor.fetchone()
        jobb_id = jobb_id[0]
        totalpris = (int(pris_tjeneste) * int(self.timer_brukt)) + int(pris_matrial)

        insert_faktura = "INSERT INTO FAKTURA(KUNDE_ID, SELJAR_ID, JOBB_ID, Dato_betaling, Total_pris) " \
                         "VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(insert_faktura, (kundeid, seljar_ID, jobb_id, betalingsdato, totalpris,))
        db.commit()

Lagrefaktura()