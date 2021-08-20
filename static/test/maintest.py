import re

from flask import Flask, render_template, redirect, send_from_directory, session,request
import os
from sqldb import connect
from createpdf import create_pdf
from datetime import date, timedelta
import sqldb as t
app = Flask(__name__)
app.secret_key = '[Kb\x16o\x05\xc7\xc5P\xd8bB/@\x81\x8b\xd8\x94\x83\xcf\xed\xf4n\xc9'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    txt = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        db = connect("Innloggingsinformasjon")
        cursor = db.cursor()
        cursor.execute("SELECT BrukerID, Epost, Passord FROM innloggingsinfo WHERE Epost = %s AND Passord =%s",
                       (username, password))
        user = cursor.fetchone()

        if user:
            session['innlogga'] = True
            session['id'] = user[0]
            session['bruker'] = user[1]
            return redirect("/faktura")

        else:
            txt = "Brukarnamn/passord eksisterer ikkje"

    return render_template("login.html", txt=txt)


@app.route('/faktura', methods=['POST', 'GET'])
def faktura():
    if 'innlogga' in session:
        db = connect("faktura")
        cursor = db.cursor()
        brukar = session['bruker']
        db1 = connect("Innloggingsinformasjon")
        cursordb1 = db1.cursor()
        txt = ''
        if request.method == 'POST' and 'Kunde_namn' in request.form and 'Kunde_epost' in request.form \
                and 'Kundeadresse' in request.form \
                and 'kundens_by' in request.form and 'kundens_postnr' in request.form and 'tjeneste' in request.form \
                and 'Timerbrukt' in request.form and 'Matrial' in request.form:
                kunde_namn = request.form['Kunde_namn']
                kunde_epost = request.form['Kunde_epost']
                kunde_adresse= request.form['Kundeadresse']
                kunde_by = request.form['kundens_by']
                kunde_postnr = request.form['kundens_postnr']
                tjeneste = request.form['tjeneste']
                timer_brukt = request.form['Timerbrukt']
                matrial = request.form['Matrial']


                cursor.execute("SELECT * FROM KUNDE WHERE Namn = %s AND Epost =%s AND Adresse =%s "
                               "AND POSTKODE_PostNR =%s",
                               (kunde_namn, kunde_epost, kunde_adresse, kunde_postnr))
                kunde = cursor.fetchall()
                cursor.execute("SELECT * FROM POSTNR WHERE Postkode =%s",(kunde_postnr,))
                postnr = cursor.fetchall()
                cursor.execute("SELECT PRIS from MATRIAL WHERE ID = %s",(matrial,))
                pris_matrial = cursor.fetchone()
                cursordb1.execute("SELECT TILSETTINFO_TilsettID FROM innloggingsinfo WHERE Epost =%s", (brukar,))
                ansattid = cursordb1.fetchone()
                ansattid = ansattid[0]



                pris_matrial = pris_matrial[0]
                cursor.execute("SELECT PRIS from TJENESTE WHERE ID = %s",(tjeneste,))
                pris_tjeneste = cursor.fetchone()
                pris_tjeneste = pris_tjeneste[0]

                dato = date.today()
                betalingsdato = dato+timedelta(days=21)
                seljar_ID = 1


                if len(kunde_namn) < 3:
                  txt = "navne på kunden må være lenger enn 3 karakterer"
                elif not any(map(str.isdigit, kunde_adresse)) or not any(map(str.isalpha, kunde_adresse)) :
                    txt = "adressa må inneholde tal og bokstaver"
                elif len(kunde_postnr) !=4 or not kunde_postnr.isdigit():
                    txt = "postnummeret må inneholde fire tall"
                elif not re.match('[A-Åa-å]',kunde_by):
                    txt = "navnet på by må inneholde bare små eller store bokstaver"
                elif not timer_brukt.isdigit():
                    txt = "antall timer må være tall"
                elif postnr and kunde:

                    # send_til_db = t.Lagrefaktura(kunde_by, kunde_namn, kunde_epost, kunde_adresse, kunde_postnr, timer_brukt,
                    #                               ansattid, matrial, tjeneste)
                    # send_til_db.kunde_postnr
                    cursor.execute("SELECT ID FROM KUNDE WHERE Namn = %s AND Adresse =%s "
                                   "AND POSTKODE_PostNR =%s",
                                   (kunde_namn, kunde_adresse, kunde_postnr))
                    kundeid = cursor.fetchone()
                    kundeid = kundeid[0]

                    cursor.execute("INSERT INTO JOBB(Timer_brukt, TILSETTINFO_TilsettID, MATRIAL_ID, TJENESTE_ID, Dato)"
                                   "VALUES (%s,%s,%s,%s,%s)", (timer_brukt, ansattid, matrial, tjeneste, dato,))
                    db.commit()

                    cursor.execute("SELECT ID FROM JOBB ORDER BY ID DESC LIMIT 1")
                    jobb_id = cursor.fetchone()
                    jobb_id = jobb_id[0]
                    totalpris = (int(pris_tjeneste) * int(timer_brukt)) + int(pris_matrial)

                    cursor.execute("INSERT INTO FAKTURA(KUNDE_ID, SELJAR_ID, JOBB_ID, Dato_betaling, Total_pris) "
                                   "VALUES (%s,%s,%s,%s,%s)", (kundeid, seljar_ID, jobb_id, betalingsdato, totalpris,))
                    db.commit()

                    cursor.execute("SELECT ID FROM FAKTURA ORDER BY ID DESC LIMIT 1")
                    faktura_id = cursor.fetchall()
                    faktura_id = faktura_id[0]
                    create_pdf(faktura_id)

                    return redirect('/faktura/displaylast')


                elif not kunde and not postnr:
                    # send_til_db = t.Lagrefaktura(kunde_by, kunde_namn, kunde_epost, kunde_adresse, kunde_postnr,
                    #                              timer_brukt, ansattid, matrial, tjeneste)
                    # send_til_db.ikkje_kunde_postnr()
                    cursor.execute("INSERT INTO POSTNR(Postkode, by_namn) VALUES (%s,%s)",(kunde_postnr, kunde_by,))
                    db.commit()
                    cursor.execute("INSERT INTO KUNDE(Namn, Epost, Adresse, POSTKODE_PostNR) VALUES (%s,%s,%s,%s)",
                                   (kunde_namn, kunde_epost, kunde_adresse, kunde_postnr,))
                    db.commit()
                    cursor.execute("INSERT INTO JOBB(Timer_brukt, TILSETTINFO_TilsettID, MATRIAL_ID, TJENESTE_ID, Dato)"
                                   "VALUES (%s,%s,%s,%s,%s)", (timer_brukt, ansattid, matrial, tjeneste, dato,))
                    db.commit()

                    cursor.execute("SELECT ID FROM JOBB ORDER BY ID DESC LIMIT 1")
                    jobb_id = cursor.fetchone()
                    jobb_id =jobb_id[0]
                    cursor.execute("SELECT ID FROM KUNDE ORDER BY ID DESC LIMIT 1")
                    kunde_id = cursor.fetchone()
                    kunde_id = kunde_id[0]
                    totalpris = (int(pris_tjeneste) * int(timer_brukt)) + int(pris_matrial)

                    cursor.execute("INSERT INTO FAKTURA(KUNDE_ID, SELJAR_ID, JOBB_ID, Dato_betaling, Total_pris) "
                                   "VALUES (%s,%s,%s,%s,%s)", (kunde_id, seljar_ID, jobb_id, betalingsdato, totalpris,))
                    db.commit()
                    cursor.execute("SELECT ID FROM FAKTURA ORDER BY ID DESC LIMIT 1")
                    faktura_id = cursor.fetchone()
                    faktura_id = faktura_id[0]
                    create_pdf(faktura_id)

                    return redirect('/faktura/displaylast')

                elif postnr and not kunde:
                    # send_til_db = t.Lagrefaktura(kunde_by, kunde_namn, kunde_epost, kunde_adresse, kunde_postnr,
                    #                              timer_brukt,
                    #                              ansattid, matrial, tjeneste)
                    # send_til_db.postnr_ikkje_kunde()
                    cursor.execute("INSERT INTO KUNDE(Namn, Epost, Adresse, POSTKODE_PostNR) VALUES (%s,%s,%s,%s)",
                                   (kunde_namn, kunde_epost, kunde_adresse, kunde_postnr,))
                    db.commit()
                    cursor.execute("INSERT INTO JOBB(Timer_brukt, TILSETTINFO_TilsettID, MATRIAL_ID, TJENESTE_ID, Dato)"
                                   "VALUES (%s,%s,%s,%s,%s)", (timer_brukt, ansattid, matrial, tjeneste, dato,))
                    db.commit()

                    cursor.execute("SELECT ID FROM JOBB ORDER BY ID DESC LIMIT 1")
                    jobb_id = cursor.fetchone()
                    jobb_id = jobb_id[0]
                    cursor.execute("SELECT ID FROM KUNDE ORDER BY ID DESC LIMIT 1")
                    kunde_id = cursor.fetchone()
                    kunde_id = kunde_id[0]
                    totalpris = (int(pris_tjeneste) * int(timer_brukt)) + int(pris_matrial)

                    cursor.execute("INSERT INTO FAKTURA(KUNDE_ID, SELJAR_ID, JOBB_ID, Dato_betaling, Total_pris) "
                                   "VALUES (%s,%s,%s,%s,%s)", (kunde_id, seljar_ID, jobb_id, betalingsdato, totalpris,))
                    db.commit()
                    cursor.execute("SELECT ID FROM FAKTURA ORDER BY ID DESC LIMIT 1")
                    faktura_id = cursor.fetchone()
                    faktura_id = faktura_id[0]
                    create_pdf(faktura_id)
                    return redirect('/faktura/displaylast')


        return render_template("faktura.html", username=session['bruker'], txt = txt)

    return redirect("/")


@app.route('/newuser', methods=['GET', 'POST'])
def new_user():
    msg = ''
    if request.method == 'POST' and 'tilsettid' in request.form and 'nytt_passord' in request.form and 'epost' in request.form:
        username = request.form['epost']
        password = request.form['nytt_passord']
        tilsettid = request.form['tilsettid']
        db = connect("Innloggingsinformasjon")
        cursor = db.cursor()
        cursor.execute(f"SELECT tilsettid from tilsettinfo where tilsettid = %s", (tilsettid,))
        db_tilsettid = cursor.fetchall()
        cursor.execute(f"SELECT TILSETTINFO_TilsettID from innloggingsinfo where TILSETTINFO_TilsettID = %s",
                        (tilsettid,))
        user_exist = cursor.fetchall()
        cursor.execute(f"SELECT epost from innloggingsinfo where epost = %s",
                        (username,))
        epost_exist = cursor.fetchall()
        if not db_tilsettid:#sjekker om ansattide oppgitt er i tilsettinfotabellen
            msg = "AnsattID er ikkje valid, mener du dette er feil kontakt sjefen"
        elif re.search("@consultas.no", username) == None: #sjekker om eposten som er oppgitt stemmer overens med eposten som blir brukt i bedrifta
             msg = "Epost matcher ikkje bedriftsepost, denne er dittnavn@consultas.no"
        elif user_exist: # sjekker om det allereie er opretta ein brukar med samme tilsettid
            msg = "Du har alt ein brukar"
        elif epost_exist:
            msg = "eposten er i bruk"
        else: #om tilsettiden finnast tilsettinfotabellen, eposten har riktig format og det ikkje er opretta ein brukar med tilsettID blir det oppretta ein brukar
            registreringsinfo = (tilsettid, username, password)
            cursor.execute("INSERT INTO innloggingsinfo(Tilsettinfo_tilsettID, Epost, Passord) Values (%s,%s,%s)",
                           registreringsinfo)
            db.commit()
            msg = "du har blitt registrert"
    elif request.method == 'POST':
        msg = 'fyll ut alle felta'
    return render_template("newuser.html", msg=msg)


@app.route('/faktura/logout')
def loggut():
    session.pop('innlogga', None)
    session.pop('id', None)
    session.pop('bruker', None)
    return redirect("/")

# @app.route('/faktura/invoice')
# def invoice():
#
#     if 'innlogga' in session:
#
#         db = connect("faktura")
#         cursor = db.cursor()
#         cursor.execute("SELECT ID FROM FAKTURA ORDER BY ID DESC LIMIT 1")
#         faktura_id = cursor.fetchone()
#         faktura_id = faktura_id[0]
#         pdf = f"Faktura{faktura_id}.pdf"
#         create_pdf(faktura_id)
#         workingdir = os.path.abspath(os.getcwd())
#
#         return render_template("invoices.html", session=session, pdf=pdf)
#     return redirect("/")


@app.route('/faktura/displaylast', methods=['GET', 'POST'])
def displaytheinvoices():
    if 'innlogga' in session:
        db = connect("faktura")
        cursor = db.cursor()
        cursor.execute("SELECT ID FROM FAKTURA ORDER BY ID DESC LIMIT 1")
        faktura_id = cursor.fetchone()
        faktura_id = faktura_id[0]
        if request.method == 'POST' and 'lagre' in request.form:
            svar = request.form['lagre']
            if svar == "ja":
                return redirect('/faktura')
            if svar == "nei":
                cursor.execute("DELETE FROM FAKTURA ORDER BY ID DESC LIMIT 1")
                db.commit()
                cursor.execute("DELETE FROM JOBB ORDER BY ID DESC LIMIT 1")
                db.commit()
                try:
                    os.remove(f"./static/Faktura{faktura_id}.pdf")
                except:
                    return "Fila som skal slettast er ikkje funne"
                return redirect('/faktura')




        return render_template("latestinvoice.html", id=faktura_id)
    return redirect("/")
# @app.route('/diplaylast')
# def displaytheinvoices():
#     db = connect("faktura")
#     cursor = db.cursor()
#     cursor.execute("SELECT ID FROM FAKTURA ORDER BY ID DESC LIMIT 1")
#     faktura_id = cursor.fetchone()
#     faktura_id = faktura_id[0]
#
#     return render_template("displayinvoice2.html", id=faktura_id)






if __name__ == '__main__':
    app.run(debug=True)