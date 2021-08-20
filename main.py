import re
from argon2 import PasswordHasher, Type
from flask import Flask, render_template, redirect, session, request
import os
from sqldb import connect
import sqldb as t


app = Flask(__name__)
app.secret_key = '[Kb\x16o\x05\xc7\xc5P\xd8bB/@\x81\x8b\xd8\x94\x83\xcf\xed\xf4n\xc9'


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])  # opprette kopling mellom url og funksjonen under
def login():
    txt = ''  # opprette variabel som ikkje ineholder noe
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']  # hente ned opplysningar gitt frå bruker
        password = request.form['password']  # hente ned opplysningar gitt frå bruker
        db = connect("Innloggingsinformasjon")  # kople til database
        cursor = db.cursor(prepared=True)  # opprette ein cursor som tillet gjennomføring av førebudde setningar
        # SQL spørjing som setter innformajonen inn i riktig tabell i databasen
        finne_bruker = "SELECT BrukerID, Epost, Passord FROM innloggingsinfo WHERE Epost = %s"  # sql spørjing som
        # henter infor frå database
        cursor.execute(finne_bruker, (username,))  #utføre sql spørjing
        user = cursor.fetchone()  # hente resultat frå spørjingen
        if user:  # sjekke om brukarnamn finnast
            db_passord = user[2]  # sette variabelen db_passord lik den tredje verdien i tuplen som er lagra i user variabel
            ph = PasswordHasher(
                memory_cost=65636,
                time_cost=4,
                parallelism=2,
                salt_len=16,
                hash_len=32,
                type=Type.ID)  # definere parameter for pasword hasher
            try:
                ph.verify(db_passord, password)  # vertifisere passord
                if ph.check_needs_rehash(db_passord):  # sjekker om hashen i datbasen må hashast på nytt
                    passwordhash = ph.hash(password)  # hashe passordet på nytt om det er nødvendig
                    oppdater_hash = "UPDATE innloggingsinfo SET Passord = %s WHERE BrukerID =%s"  # spøring som oppdatere db
                    cursor.execute(oppdater_hash, (passwordhash, user[0],))  # utføre spørjing
                melding = "rett"  # sette variabelen til rett
            except:
                melding = "feil_passord"  # om passordet ikkje blir vertifisert vil det bli sendt ut ei feil melding og
                #melding blir satt til feil_passord
            if user and melding == "rett":  # sjekke om brukernman er i database og at passordet er vertifisert
                session['innlogga'] = True  # sette session innlogga til sann
                session['id'] = user[0]  # sette session id lik brukerid
                session['bruker'] = user[1]  # sette session bruker lik brukernamn
                return redirect("/faktura")
            else:
                txt = "Brukarnamn/passord eksisterer ikkje"  # om ikkje skal denne stringen visast på sida
        else:
            txt = "finner ikkje bruker"
    return render_template("login.html", txt=txt)  # gjengi malen login.html


@app.route('/faktura', methods=['POST', 'GET'])  # opprette kopling mellom url og funksjonen under
def faktura():
    if 'innlogga' in session:  # sjekke om brukar er innlogga
        db = connect("faktura")   # kople til database
        cursor = db.cursor(prepared=True)  # opprette ein cursor som tillet gjennomføring av førebudde setningar
        # SQL spørjing som setter innformajonen inn i riktig tabell i databasen
        brukar = session['bruker']
        db1 = connect("Innloggingsinformasjon")    # kople til database
        cursordb1 = db1.cursor(prepared=True)  # opprette ein cursor som tillet gjennomføring av førebudde setningar
        # SQL spørjing som setter innformajonen inn i riktig tabell i databasen
        txt = ''  # opprette ein variabel kalla txt
        if request.method == 'POST' and 'Kunde_namn' in request.form and 'Kunde_epost' in request.form \
                and 'Kundeadresse' in request.form \
                and 'kundens_by' in request.form and 'kundens_postnr' in request.form and 'tjeneste' in request.form \
                and 'Timerbrukt' in request.form and 'Matrial' in request.form:
            kunde_namn = request.form['Kunde_namn']  # hente ned opplysningar gitt frå bruker
            kunde_epost = request.form['Kunde_epost']  # hente ned opplysningar gitt frå bruker
            kunde_adresse = request.form['Kundeadresse']  # hente ned opplysningar gitt frå bruker
            kunde_by = request.form['kundens_by']  # hente ned opplysningar gitt frå bruker
            kunde_postnr = request.form['kundens_postnr']  # hente ned opplysningar gitt frå bruker
            tjeneste = request.form['tjeneste']  # hente ned opplysningar gitt frå bruker
            timer_brukt = request.form['Timerbrukt']  # hente ned opplysningar gitt frå bruker
            matrial = request.form['Matrial']  # hente ned opplysningar gitt frå bruker

            finne_kunde = "SELECT * FROM KUNDE WHERE Namn = %s AND Epost =%s AND Adresse =%s " \
                          "AND POSTKODE_PostNR =%s"  # spøring som henter data frå database
            cursor.execute(finne_kunde, (kunde_namn, kunde_epost, kunde_adresse, kunde_postnr))  # utføre spørrjing
            kunde = cursor.fetchall()  # fange reslutat av spørjinga
            finne_postnr = "SELECT * FROM POSTNR WHERE Postkode =%s"   # spøring som henter data frå database
            cursor.execute(finne_postnr, (kunde_postnr,))   # utføre spørrjing
            postnr = cursor.fetchall()   # fange reslutat av spørjinga
            finne_ansattid = "SELECT TILSETTINFO_TilsettID FROM innloggingsinfo WHERE Epost =%s"    # spøring som
            # henter data frå database
            cursordb1.execute(finne_ansattid, (brukar,))  # utføre spørrjing
            ansattid = cursordb1.fetchone()  # fange reslutat av spørjinga
            ansattid = ansattid[0]  # sette variabelen asattid lik den første verdien i resultatet av spørjinga

            if len(kunde_namn) < 3:  # sjekke om kundenamn er lenger enn tre karakterar
                txt = "navne på kunden må være lenger enn 3 karakterer"

                # sjekke om kundeadresse inneheld bokstavar og tal
            elif not any(map(str.isdigit, kunde_adresse)) or not any(map(str.isalpha, kunde_adresse)):
                txt = "adressa må inneholde tal og bokstaver"
            elif len(kunde_postnr) != 4 or not kunde_postnr.isdigit():  # sjekker om postnr inneheld tal og ikkje = 4
                txt = "postnummeret må inneholde fire tall"
            elif not re.match('[A-Åa-å]', kunde_by):  # sjekker om by inneheld noko anna enn bokstavar
                txt = "navnet på by må inneholde bare små eller store bokstaver"
            elif not timer_brukt.isdigit():  # sjekker om timer_brukt inneholde noko anna enn tal
                txt = "antall timer må være tall"
            elif postnr and kunde:  # sjekker om postnummer og kunde er i database
                send_til_db = t.Lagrefaktura(kunde_by, kunde_namn, kunde_epost, kunde_adresse, kunde_postnr,
                                             timer_brukt, ansattid, matrial, tjeneste) # lage ein instans av lagrefaktura
                send_til_db.kundepostnr()  # kalle på metoden postnr_ikkje_kunde()
                return redirect('/faktura/displaylast')  # sender bruker til URL-en /faktura/displaylast


            elif not kunde and not postnr:  # sjekker om verken kunde eller postnr er i database
                send_til_db = t.Lagrefaktura(kunde_by, kunde_namn, kunde_epost, kunde_adresse, kunde_postnr,
                                             timer_brukt, ansattid, matrial, tjeneste) # lage ein instans av lagrefaktura
                send_til_db.ikkje_kunde_postnr()  # kalle på metoden postnr_ikkje_kunde()
                return redirect('/faktura/displaylast')  # sender bruker til URL-en /faktura/displaylast

            elif postnr and not kunde:  # sjekker om postnr er i databasen og om kunde ikkje er i database
                send_til_db = t.Lagrefaktura(kunde_by, kunde_namn, kunde_epost, kunde_adresse, kunde_postnr,
                                             timer_brukt, ansattid, matrial, tjeneste)  # lage ein instans av lagrefaktura
                send_til_db.postnr_ikkje_kunde()  # kalle på metoden postnr_ikkje_kunde()

                return redirect('/faktura/displaylast')  # sender bruker til URL-en /faktura/displaylast

        return render_template("faktura.html", username=session['bruker'], txt=txt)

    return redirect("/")


@app.route('/newuser', methods=['GET', 'POST'])
def new_user():
    msg = ''
    if request.method == 'POST' and 'tilsettid' in request.form and 'nytt_passord' in request.form \
            and 'epost' in request.form:

        username = request.form['epost']  # hente ned opplysningar gitt frå bruker
        password = request.form['nytt_passord']  # hente ned opplysningar gitt frå bruker
        tilsettid = request.form['tilsettid']  # hente ned opplysningar gitt frå bruker

        db = connect("Innloggingsinformasjon")  # kople til database
        cursor = db.cursor(prepared=True)  # opprette ein cursor som tillet gjennomføring av førebudde setningar
        # SQL spørjing som setter innformajonen inn i riktig tabell i databasen
        hente_ansattid = "SELECT tilsettid from tilsettinfo where tilsettid = %s"  # spørjing som henter info frå db
        cursor.execute(hente_ansattid, (tilsettid,))  # utføre spørrjing
        db_tilsettid = cursor.fetchall()  # fange resultat frå spørjing
        sjekke_tilsettid = "SELECT TILSETTINFO_TilsettID from innloggingsinfo where TILSETTINFO_TilsettID = %s"   #
        # spørjing som henter info frå db
        cursor.execute(sjekke_tilsettid, (tilsettid,))  # utføre spørrjing
        user_exist = cursor.fetchall()  # fange resultat frå spørjing
        sjekke_epost = "SELECT epost from innloggingsinfo where epost = %s"    # spørjing som henter info frå db
        cursor.execute(sjekke_epost, (username,))  # utføre spørrjing
        epost_exist = cursor.fetchall()  # fange resultat frå spørjing

        Spesialkarakterar = ['$', '@', '#', '%', '!']  # definere variablen som inneheld godkjente spesial karaktera
        # for passord

        if not db_tilsettid:  # sjekker om ansattide oppgitt er i tilsettinfotabellen
            msg = "AnsattID er ikkje valid, mener du dette er feil kontakt sjefen"
        # sjekker om eposten som er oppgitt stemmer overens med eposten som blir brukt i bedrifta
        elif re.search("@consultas.no", username) == None:
            msg = "Epost matcher ikkje bedriftsepost, denne er dittnavn@consultas.no"
        elif user_exist:   # sjekker om det allereie er opretta ein brukar med samme tilsettid
            msg = "Du har alt ein brukar"
        elif epost_exist:
            msg = "eposten er i bruk"
        elif not any(char in Spesialkarakterar for char in password):  # sjekke om passord inneholder spesialkarakter
            msg = "Passordet må inneholde ein spesial karakter ($,@,#,%,!)"
        elif re.search('[0-9]',password) is None:  # sjekke om passord inneholder tall
            msg = "Passordet må inneholde minst eit tall"
        elif re.search("[a-z]", password) is None:  # sjekke om passord inneholder små bokstaver
            msg = "Passordet må inneholde minst ein liten bokstav"
        elif re.search("[A-Z]", password) is None:  # sjekke om passord inneholder store bokstaver
            msg = "Passordet må inneholde minst ein stor bokstav"
        elif len(password) <= 12:  # sjekke om passord er minst 12 karaktere langt
            msg = "Passordet er for kort, minste lengda er 12 karaktera"
        # om tilsettiden finnast tilsettinfotabellen, eposten har riktig format og det ikkje er opretta ein brukar
        # med tilsettID blir det oppretta ein brukar
        else:
            ph = PasswordHasher(
                memory_cost=65636,
                time_cost=4,
                parallelism=2,
                salt_len=16,
                hash_len=32,
                type=Type.ID)  # definere parameter for pasword hasher
            hsh = ph.hash(password)  # hashe passord
            db_send = t.Lagrebrukarinfo(tilsettid, username, hsh)  # lage ein instans av klassen lagrebrukarinfo
            db_send.user()  # kalle på metoden user
            msg = "Du har blitt registrert"  # sette variabel msg til meldinga "du har blitt registrert#

    return render_template("newuser.html", msg=msg)


@app.route('/faktura/logout')
def loggut():
    session.pop('innlogga', None)  # fjerne innlogga frå økt om det er der
    session.pop('id', None)  # fjerne id frå økt om det er der
    session.pop('bruker', None)  # fjerne bruker frå økt om det er der
    return redirect("/")


@app.route('/faktura/displaylast', methods=['GET', 'POST'])
def displaytheinvoices():
    if 'innlogga' in session:
        db = connect("faktura")
        cursor = db.cursor(prepared=True)  # opprette ein cursor som tillet gjennomføring av førebudde setningar
        # SQL spørjing som setter innformajonen inn i riktig tabell i databasen
        hente_fakturaid = "SELECT ID FROM FAKTURA ORDER BY ID DESC LIMIT 1"   # spørjing som henter info frå db
        cursor.execute(hente_fakturaid)  # køyre spørjing
        faktura_id = cursor.fetchone()  # hente resultat av spørjing
        faktura_id = faktura_id[0]
        if request.method == 'POST' and 'lagre' in request.form:
            svar = request.form['lagre']   # hente ned opplysningar gitt frå bruker
            if svar == "ja":
                return redirect('/faktura')  # sende bruker tilbake til /faktura
            if svar == "nei":
                slette_faktura = "DELETE FROM FAKTURA ORDER BY ID DESC LIMIT 1"  # spørjing som slettar data fra
                # faktura tabellen
                cursor.execute(slette_faktura)  # køyre spørjing
                db.commit()  # lagre endringar i database
                slette_jobb = "DELETE FROM JOBB ORDER BY ID DESC LIMIT 1"  # spørjing som slettar data fra
                # jobb tabellen
                cursor.execute(slette_jobb)  #køyre spørjing
                db.commit()  # lagre endringar i database
                try:
                    os.remove(f"./static/Faktura{faktura_id}.pdf")  # slette PDF frå maskin
                except:
                    return "Fila som skal slettast er ikkje funne"
                return redirect('/faktura')  # sende bruker til /faktura

        return render_template("latestinvoice.html", id=faktura_id)
    return redirect("/")
@app.route('/visfaktura', methods=['GET', 'POST'])
def visfaktura():
    if 'innlogga' in session:  # sjekke om brukar er innlogga
        faktura_nummer = 1  # opprette ein varibel og sette den lik 1
        if request.method == 'POST' and 'faktura_nummer' in request.form:
            faktura_nummer= request.form['faktura_nummer']   # hente ned opplysningar gitt frå bruker
            if re.search('[0-9]', faktura_nummer):  # sjekke om brukar input er tal
                if not os.path.isfile(f"static/faktura{faktura_nummer}.pdf"):  # sjekke om fil ikkje eksisterer
                    txt = "finner ikkje fakturaen du ønsker å sjå, sjekk om du har skreve riktig faktura nummer"
                else:
                    txt = ""
            else:
                txt = "Du må skrive et tall"
            return render_template("visfaktura.html", id=faktura_nummer, txt=txt)


    return render_template("visfaktura.html", id=faktura_nummer)

if __name__ == '__main__':
    app.run(debug=True)  # køyre applikasjon
