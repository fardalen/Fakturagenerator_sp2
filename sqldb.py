import mysql.connector as mysql
from datetime import date, timedelta
from reportlab.pdfgen.canvas import Canvas
import os


# starter med faktura id
def create_pdf(faktura_id):
    """funksjon som genere faktura"""

    db = connect("faktura")  # kople til database
    cursor = db.cursor(prepared=True)  # opprette ein cursor som tillet gjennomføring av førebudde setningar
    # SQL spørjing som setter henter informasjon frå databasen
    hente_kundeinfo = "SELECT kunde.namn, kunde.Epost, kunde.Adresse, POSTKODE_PostNR, POSTNR.by_namn " \
                      "FROM faktura " \
                      "INNER JOIN kunde ON FAKTURA.KUNDE_ID = KUNDE.ID " \
                      "INNER JOIN POSTNR ON KUNDE.POSTKODE_PostNR = POSTNR.Postkode " \
                      "WHERE FAKTURA.ID = %s " \
                      "GROUP BY FAKTURA.ID"
    cursor.execute(hente_kundeinfo, (faktura_id,))  # utfører SQL spørjingen
    kunde_info = cursor.fetchone()  # henter resultatet frå spørjinga
    # SQL spørjing som setter henter informasjon frå databasen
    hente_seljarinfo = "SELECT SELJAR.namn, SELJAR.Adresse, SELJAR.kontonummer, SELJAR.organisjonnr, " \
                       "POSTKODE_PostNR, POSTNR.by_namn " \
                       "FROM faktura " \
                       "INNER JOIN SELJAR ON FAKTURA.SELJAR_ID = SELJAR.ID " \
                       "INNER JOIN POSTNR ON SELJAR.POSTKODE_PostNR = POSTNR.Postkode " \
                       "WHERE FAKTURA.ID = %s " \
                       "GROUP BY FAKTURA.ID;"
    cursor.execute(hente_seljarinfo, (faktura_id,))  # utfører SQL spørjingen
    seljar_info = cursor.fetchone()  # henter resultatet frå spørjinga
    # hente ut faktura info
    hente_fakturainfo = "select ID, Dato_betaling, Total_pris FROM FAKTURA WHERE ID = %s"
    cursor.execute(hente_fakturainfo, (faktura_id,))  # utfører SQL spørjingen
    faktura_info = cursor.fetchone()  # henter resultatet frå spørjinga
    # SQL spørjing som setter henter informasjon frå databasen
    hente_jobbinfo = "SELECT jobb.Timer_brukt, jobb.dato, TJENESTE.Namn, TJENESTE.Pris, MATRIAL.namn, MATRIAL.pris " \
                     "FROM FAKTURA " \
                     "INNER JOIN jobb ON FAKTURA.Jobb_ID = jobb.ID " \
                     "INNER JOIN TJENESTE ON JOBB.TJENESTE_ID = TJENESTE.ID " \
                     "INNER JOIN MATRIAL ON JOBB.MATRIAL_ID = MATRIAL.ID " \
                     "WHERE FAKTURA.ID = %s " \
                     "GROUP BY FAKTURA.ID;"
    cursor.execute(hente_jobbinfo, (faktura_id,))
    jobbinfo = cursor.fetchone()
    # hente riktig data ut av tupelen
    kunde_namn = kunde_info[0]
    kunde_epost = kunde_info[1]
    kunde_adresse = kunde_info[2]
    kunde_postkode = kunde_info[3]
    kunde_by = kunde_info[4]
    seljar_namn = seljar_info[0]
    seljar_adresse = seljar_info[1]
    seljar_konto = seljar_info[2]
    seljar_organisasjonsnr = seljar_info[3]
    seljar_poskode = seljar_info[4]
    seljar_by = seljar_info[5]
    fakturaid = faktura_info[0]
    betalingsdato = faktura_info[1]
    totalpris = faktura_info[2]
    timer_brukt = jobbinfo[0]
    dato_opretta = jobbinfo[1]
    tjeneste_namn = jobbinfo[2]
    tjeneste_pris = jobbinfo[3]
    matrial_namn = jobbinfo[4]
    matrial_pris = jobbinfo[5]
    totalpris_tjeneste = int(tjeneste_pris) * int(timer_brukt)
    nettopris = totalpris / (1.25)
    mva = totalpris - nettopris

    filename = f"static/Faktura{faktura_id}.pdf"

    if os.path.exists(filename):
        return "det er allerede opretta en faktura for denne"

    pdf = Canvas(filename)
    # sette inn verdiar i PDF og bestemme plassering på verdiane i PDF fil
    pdf.setTitle('invoice')
    pdf.drawImage("static/image.png", 30, 700, width=150, height=100)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(520, 800, "FAKTURA")
    pdf.setFont("Times-Roman", 12)
    pdf.drawString(30, 670, kunde_namn)
    pdf.drawString(30, 655, kunde_adresse)
    pdf.drawString(30, 640, f"{kunde_postkode} {kunde_by}")
    pdf.drawString(350, 785, "------------------------------------------------------")
    pdf.drawString(350, 770, seljar_namn)
    pdf.drawString(350, 755, seljar_adresse)
    pdf.drawString(350, 740, seljar_organisasjonsnr)
    pdf.drawString(350, 725, f"{str(seljar_poskode)} {seljar_by}")
    pdf.drawString(350, 710, "------------------------------------------------------")
    pdf.setFont("Times-Roman", 10)
    pdf.drawString(350, 695, f"Leveringsdato: {str(dato_opretta)}")
    pdf.drawString(350, 680, f"Levert til: {kunde_adresse}, {kunde_postkode}, {kunde_by}")
    pdf.setFont("Times-Roman", 12)
    pdf.drawString(350, 670, "------------------------------------------------------")
    pdf.drawString(350, 655, f"Fakturadato: {str(dato_opretta)}")
    pdf.drawString(350, 640, f"Fakturnr: {str(fakturaid)}")
    pdf.drawString(350, 625, f"Forfallsdato: {str(betalingsdato)}")
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(30, 600, "BESKRIVELSE")
    pdf.drawString(300, 600, "PRIS")
    pdf.drawString(375, 600, "ANTALL")
    pdf.drawString(450, 600, "MVA")
    pdf.drawString(525, 600, "Beløp")
    pdf.setFont("Times-Roman", 12)
    pdf.drawString(0, 590,
                   "----------------------------------------------------------------------------------------------")
    pdf.drawString(300, 590, "-------------------------------------------------------------------------")
    pdf.drawString(30, 575, tjeneste_namn)
    pdf.drawString(30, 545, matrial_namn)
    pdf.drawString(300, 575, str(tjeneste_pris))
    pdf.drawString(300, 545, str(matrial_pris))
    pdf.drawString(375, 575, str(timer_brukt))
    pdf.drawString(375, 545, "1")
    pdf.drawString(450, 575, "25%")
    pdf.drawString(450, 545, "25%")
    pdf.drawString(525, 575, str(totalpris_tjeneste))
    pdf.drawString(525, 545, str(matrial_pris))
    pdf.drawString(0, 535,
                   "----------------------------------------------------------------------------------------------")
    pdf.drawString(300, 535, "-------------------------------------------------------------------------")
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(30, 520, "MVA-sats")
    pdf.drawString(115, 520, "Grunnlag")
    pdf.drawString(200, 520, "MVA")
    pdf.setFont("Times-Roman", 10)
    pdf.drawString(30, 505, "25%")
    pdf.drawString(115, 505, str(nettopris))
    pdf.drawString(200, 505, str(mva))
    pdf.drawString(290, 520, "Nettobeløp:")
    pdf.drawString(290, 505, "Meirverdiavgift:")
    pdf.drawString(525, 520, str(nettopris))
    pdf.drawString(525, 505, str(mva))
    pdf.drawString(290, 495,
                   "-----------------------------------------------------------------------------------------")
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(290, 475, "Å BETALE")
    pdf.drawString(500, 475, str(totalpris))
    pdf.drawString(30, 150, "BETALINGSINFORMAJON")
    pdf.setFont("Times-Roman", 12)
    pdf.drawString(0, 140,
                   "----------------------------------------------------------------------------------------------")
    pdf.drawString(300, 140, "-------------------------------------------------------------------------")
    pdf.setFont("Times-Roman", 10)
    pdf.drawString(30, 130, f"Fakturanummer: {faktura_id}")
    pdf.drawString(30, 115, f"Sum å betale: {totalpris}")
    pdf.drawString(300, 130, f"Bankonto: {seljar_konto}")

    pdf.save()  # lagre PDF fil


def connect(db_name):
    """funksjon som opprettar tilkopling til ein database"""

    try:
        with open('config', 'r') as f:  # opne ei fil kalla config i lese modus
            innhold = f.readlines()  # lese innholde i fila
            user = innhold[0]  # sette variabelen user lik den første verdien i fila cofig
            passw = innhold[1]  # sette variabelen passw lik den andre verdien i fila config
        return mysql.connect(  # oppretter ein tilkopling til MySQL serveren
            host='localhost',  # setter vert lik lokalvert(127.0.0.1)
            user=user,  # setter user lik variabelen user
            password=passw,  # setter password lik variabelen passwd
            database=db_name)  # setter database lik db_name variabelen
    except mysql.Error as err:  # fange syntaks error
        print(f'Noko gjekk feil: {err}')


class Lagrebrukarinfo:
    """Klasse som lagrar brukar innformasjon i database """

    # definerer __init__ metoden med parametera self, tilsettid, epost og passord
    def __init__(self, tilsettid, epost, passord):
        self.tilsettid = tilsettid
        self.epost = epost
        self.passord = passord

    def user(self):
        """Metode som kan lagre innformasjon om brukara i database"""

        db = connect("innloggingsinformasjon")  # kople til database
        cursor = db.cursor(prepared=True)  # opprette ein cursor som tillet gjennomføring av førebudde setningar

        stmt = "INSERT INTO innloggingsinfo(Tilsettinfo_tilsettID, Epost, Passord) Values (%s,%s,%s)"  # SQL spørjing
        # som setter innformajonen inn i riktig tabell i databasen
        cursor.execute(stmt, (self.tilsettid, self.epost, self.passord,))  # utfører SQL spørjingen satt over og setter
        # inn verdiane tilsettid, epost og passord i spørjinga.
        db.commit()  # sende ein begå kommando til databasen


class Lagrefaktura:
    """klasse som lagra opplysningar om faktura i database"""

    # definerer __init__ metoden med parametera self, tilsettid, epost og passord
    def __init__(self, kunde_by, kunde_namn, kunde_epost, kunde_adresse, kunde_postnr, timer_brukt, ansattid, matrial,
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
        """Metode som lagrar innfo om jobb, faktura, kunde og postnummer i database"""

        db = connect("faktura")  # kople til database
        cursor = db.cursor(prepared=True)  # opprette ein cursor som tillet gjennomføring av førebudde setningar
        # SQL spørjing som setter innformajonen inn i riktig tabell i databasen

        dato = date.today()  # hente dagens dato
        betalingsdato = dato + timedelta(days=21)  # hente dato 21 dagar fram i tid
        seljar_ID = 1  # sette seljar_ID til 1

        hente_mpris = "SELECT PRIS from MATRIAL WHERE ID = %s"  # SQL spørjing som setter innformajonen inn i riktig
        # tabell i databasen
        cursor.execute(hente_mpris, (self.matrial,))  # utfører SQL spørjingen satt over og setter
        # inn verdien matrial i spørjinga.
        pris_matrial = cursor.fetchone()  # henter resultatet frå spørjinga

        pris_matrial = pris_matrial[0]  # setter variabelen pris_matrial lik den første verdien i tuplen som
        # inneholder resultatet av spørjinga
        hente_tpris = "SELECT PRIS from TJENESTE WHERE ID = %s"  # SQL spørjing som henter innformajonen frå database

        cursor.execute(hente_tpris, (self.tjeneste,))
        pris_tjeneste = cursor.fetchone()  # henter resultatet frå spørjinga
        pris_tjeneste = pris_tjeneste[0]  # setter variabelen pris_tjeneste lik den første verdien i tuplen som
        # inneholder resultatet av spørjinga

        insert_postnr = "INSERT INTO POSTNR(Postkode, by_namn) VALUES (%s,%s)"  # SQL spørjing som setter innformajonen
        # inn i riktig tabell i databasen
        cursor.execute(insert_postnr, (self.kunde_postnr, self.kunde_by,))  # utfører SQL spørjingen
        db.commit()  # sende ein begå kommando til databasen
        insert_kunde = "INSERT INTO KUNDE(Namn, Epost, Adresse, POSTKODE_PostNR) VALUES (%s,%s,%s,%s)"  # SQL spørjing
        # som setter innformajonen inn i riktig tabell i databasen
        cursor.execute(insert_kunde, (self.kunde_namn, self.kunde_epost, self.kunde_adress, self.kunde_postnr,))  #
        # utfører SQL spørjingen
        db.commit()  # sende ein begå kommando til databasen
        insert_jobb = "INSERT INTO JOBB(Timer_brukt, TILSETTINFO_TilsettID, MATRIAL_ID, TJENESTE_ID, Dato)" \
                      " VALUES (%s,%s,%s,%s,%s)"  # SQL spørjing som setter innformajonen inn i riktig tabell i databasen
        cursor.execute(insert_jobb, (self.timer_brukt, self.ansattid, self.matrial, self.tjeneste, dato,))
        db.commit()  # sende ein begå kommando til databasen
        hente_jobb = "SELECT ID FROM JOBB ORDER BY ID DESC LIMIT 1"  # SQL spørjing som henter innformajonen frå database
        cursor.execute(hente_jobb)  # utfører SQL spørjingen
        jobb_id = cursor.fetchone()  # henter resultatet frå spørjinga
        jobb_id = jobb_id[0]  # setter variabelen jobb_id lik den første verdien i tuplen som
        # inneholder resultatet av spørjinga
        hente_kunde = "SELECT ID FROM KUNDE ORDER BY ID DESC LIMIT 1"  # SQL spørjing som henter innformajonen frå database
        cursor.execute(hente_kunde)  # utfører SQL spørjingen
        kunde_id = cursor.fetchone()  # henter resultatet frå spørjinga
        kunde_id = kunde_id[0]  # setter variabelen kunde_id lik den første verdien i tuplen som
        # inneholder resultatet av spørjinga
        totalpris = (int(pris_tjeneste) * int(self.timer_brukt)) + int(pris_matrial)  # reknar ut totalpris

        insert_faktura = "INSERT INTO FAKTURA(KUNDE_ID, SELJAR_ID, JOBB_ID, Dato_betaling, Total_pris) " \
                         "VALUES (%s,%s,%s,%s,%s)"  # SQL spørjing som setter innformajonen inn i riktig tabell i
        # databasen
        cursor.execute(insert_faktura,
                       (kunde_id, seljar_ID, jobb_id, betalingsdato, totalpris,))  # utfører SQL spørjingen
        db.commit()  # sende ein begå kommando til databasen

        cursor.execute("SELECT ID FROM FAKTURA ORDER BY ID DESC LIMIT 1")  # SQL spørjing som henter innformajonen frå
        # database
        faktura_id = cursor.fetchone()  # henter resultatet frå spørjinga
        faktura_id = faktura_id[0]  # setter variabelen faktura id den første verdien i tuplen som
        # inneholder resultatet av spørjinga
        create_pdf(faktura_id)  # kalle på create_pdf funksjonen med faktura_id som variabel

    def postnr_ikkje_kunde(self):
        """Metode som lagrar innfo om jobb, faktura, kunde i database"""

        db = connect("faktura")  # kople til database
        cursor = db.cursor(prepared=True)  # opprette ein cursor som tillet gjennomføring av førebudde setningar
        # SQL spørjing som setter innformajonen inn i riktig tabell i databasen

        dato = date.today()  # hente dagens dato
        betalingsdato = dato + timedelta(days=21)  # hente dato 21 dagar fram i tid
        seljar_ID = 1  # sette seljar_ID til 1

        hente_mpris = "SELECT PRIS from MATRIAL WHERE ID = %s"  # SQL spørjing som henter innformajonen frå database
        cursor.execute(hente_mpris, (self.matrial,))  # utfører SQL spørjingen
        pris_matrial = cursor.fetchone()  # henter resultatet frå spørjinga

        pris_matrial = pris_matrial[0]  # setter variabelen pris_matrial lik den første verdien i tuplen som
        # inneholder resultatet av spørjinga
        hente_tpris = "SELECT PRIS from TJENESTE WHERE ID = %s"  # SQL spørjing som henter innformajonen frå database
        cursor.execute(hente_tpris, (self.tjeneste,))  # utfører SQL spørjingen
        pris_tjeneste = cursor.fetchone()  # henter resultatet frå spørjinga
        pris_tjeneste = pris_tjeneste[0]  # setter variabelen pris_tjeneste lik den første verdien i tuplen som
        # inneholder resultatet av spørjinga
        insert_kunde = "INSERT INTO KUNDE(Namn, Epost, Adresse, POSTKODE_PostNR) VALUES (%s,%s,%s,%s)"
        cursor.execute(insert_kunde, (self.kunde_namn, self.kunde_epost, self.kunde_adress, self.kunde_postnr,))  #
        # utfører SQL spørjingen
        db.commit()  # sende ein begå kommando til databasen
        insert_jobb = "INSERT INTO JOBB(Timer_brukt, TILSETTINFO_TilsettID, MATRIAL_ID, TJENESTE_ID, Dato) " \
                      "VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(insert_jobb, (self.timer_brukt, self.ansattid, self.matrial, self.tjeneste, dato,))  # utføre
        # SQL spørjingen
        db.commit()  # sende ein begå kommando til databasen
        hente_jobbid = "SELECT ID FROM JOBB ORDER BY ID DESC LIMIT 1"  # SQL spørjing som henter innformajonen
        # frå database
        cursor.execute(hente_jobbid)  # utfører SQL spørjingen
        jobb_id = cursor.fetchone()  # henter resultatet frå spørjinga
        jobb_id = jobb_id[0]  # setter variabelen jobb_id lik den første verdien i tuplen som
        # inneholder resultatet av spørjinga
        hente_kundeid = "SELECT ID FROM KUNDE ORDER BY ID DESC LIMIT 1"  # SQL spørjing som henter innformajonen
        # frå database
        cursor.execute(hente_kundeid)  # utfører SQL spørjingen
        kunde_id = cursor.fetchone()  # henter resultatet frå spørjinga
        kunde_id = kunde_id[0]  # setter variabelen Kunde_id lik den første verdien i tuplen som
        # inneholder resultatet av spørjinga

        totalpris = (int(pris_tjeneste) * int(self.timer_brukt)) + int(pris_matrial)  # reknar ut totalpris

        insert_faktura = "INSERT INTO FAKTURA(KUNDE_ID, SELJAR_ID, JOBB_ID, Dato_betaling, Total_pris) " \
                         "VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(insert_faktura, (kunde_id, seljar_ID, jobb_id, betalingsdato, totalpris,))
        db.commit()  # sende ein begå kommando til databasen
        hente_fakturaid = "SELECT ID FROM FAKTURA ORDER BY ID DESC LIMIT 1"  # SQL spørjing som henter innformajonen
        # frå database
        cursor.execute(hente_fakturaid)  # henter resultatet frå spørjinga
        faktura_id = cursor.fetchone()  # henter resultatet frå spørjinga
        faktura_id = faktura_id[0]  # setter variabelen faktura id den første verdien i tuplen som
        # inneholder resultatet av spørjinga
        create_pdf(faktura_id)  # kalle på create_pdf funksjonen med faktura_id som variabel

    def kundepostnr(self):
        """Metode som lagrar innfo om jobb, faktura i database"""

        db = connect("faktura")  # kople til database
        cursor = db.cursor(prepared=True)  # opprette ein cursor som tillet gjennomføring av førebudde setningar
        # SQL spørjing som setter innformajonen inn i riktig tabell i databasen

        dato = date.today()  # hente dagens dato
        betalingsdato = dato + timedelta(days=21)  # hente dato 21 dagar fram i tid
        seljar_ID = 1  # sette seljar_ID til 1

        hente_mpris = "SELECT PRIS from MATRIAL WHERE ID = %s"  # SQL spørjing som henter innformajonen frå database
        cursor.execute(hente_mpris, (self.matrial,))  # utfører SQL spørjingen satt over og setter
        # inn verdien matrial i spørjinga.
        pris_matrial = cursor.fetchone()  # henter resultatet frå spørjinga
        pris_matrial = pris_matrial[0]  # setter variabelen pris_matrial lik den første verdien i tuplen som
        # inneholder resultatet av spørjinga

        hente_tpris = "SELECT PRIS from TJENESTE WHERE ID = %s"  # SQL spørjing som henter innformajonen frå database
        cursor.execute(hente_tpris, (self.tjeneste,))  # utfører SQL spørjingen satt over og setter
        # inn variabelen tjeneste i spørjinga.
        pris_tjeneste = cursor.fetchone()  # henter resultatet frå spørjinga
        pris_tjeneste = pris_tjeneste[0]  # setter variabelen pris_matrial lik den første verdien i tuplen som
        # inneholder resultatet av spørjinga

        hente_kunde = "SELECT ID FROM KUNDE WHERE Namn = %s AND Adresse =%s AND POSTKODE_PostNR =%s"  # SQL spørjing
        # som henter innformajonen frå database
        cursor.execute(hente_kunde, (self.kunde_namn, self.kunde_adress, self.kunde_postnr))  # utfører SQL spørjingen
        # satt over og setter inn variablane kunde_ namn, kunde_ adress og kunde_postnr i spørjinga.
        kundeid = cursor.fetchone()  # henter resultatet frå spørjinga
        kundeid = kundeid[0]  # setter variabelen kundeid lik den første verdien i tuplen som
        # inneholder resultatet av spørjinga

        insert_jobb = "INSERT INTO JOBB(Timer_brukt, TILSETTINFO_TilsettID, MATRIAL_ID, TJENESTE_ID, Dato) " \
                      "VALUES (%s,%s,%s,%s,%s)"  # SQL spørjing som setter innformajonen inn i database
        cursor.execute(insert_jobb, (self.timer_brukt, self.ansattid, self.matrial, self.tjeneste, dato,))  # utfører
        # SQL spørjingen satt over og setter inn variabelene timer_brukt, ansattid, matrial, tjeneste, dato i spørjinga.
        db.commit()  # sende ein begå kommando til databasen
        hente_jobb = "SELECT ID FROM JOBB ORDER BY ID DESC LIMIT 1"  # SQL spørjing som henter innformajonen frå
        # database
        cursor.execute(hente_jobb)  # utfører SQL spørjingen
        jobb_id = cursor.fetchone()  # henter resultatet frå spørjinga
        jobb_id = jobb_id[0]  # setter variabelen jobb_id lik den første verdien i tuplen som
        # inneholder resultatet av spørjinga
        totalpris = (int(pris_tjeneste) * int(self.timer_brukt)) + int(pris_matrial)  # reknar ut totalpris

        insert_faktura = "INSERT INTO FAKTURA(KUNDE_ID, SELJAR_ID, JOBB_ID, Dato_betaling, Total_pris) " \
                         "VALUES (%s,%s,%s,%s,%s)"  # utfører
        # SQL spørjingen satt over og setter inn variabelene timer_brukt, ansattid, matrial, tjeneste, dato i spørjinga.
        cursor.execute(insert_faktura, (kundeid, seljar_ID, jobb_id, betalingsdato, totalpris,))  # utfører SQL
        # spørjingen
        db.commit()  # sende ein begå kommando til databasen
        hent_fakturaid = "SELECT ID FROM FAKTURA ORDER BY ID DESC LIMIT 1"  # SQL spørjing som henter innformajonen frå
        # database
        cursor.execute(hent_fakturaid)  # utfører SQL spørjingen
        faktura_id = cursor.fetchone()  # henter resultatet frå spørjinga
        faktura_id = faktura_id[0]  # setter variabelen faktura id den første verdien i tuplen som
        # inneholder resultatet av spørjinga
        create_pdf(faktura_id)  # kalle på create_pdf funksjonen med faktura_id som variabel
