import argon2.exceptions
from reportlab.pdfgen.canvas import Canvas
import os

# def drawMyRuler(pdf):
#     pdf.drawString(100,810, 'x100')
#     pdf.drawString(200,810, 'x200')
#     pdf.drawString(300,810, 'x300')
#     pdf.drawString(400,810, 'x400')
#     pdf.drawString(500,810, 'x500')
#
#     pdf.drawString(10,100, 'y100')
#     pdf.drawString(10,200, 'y200')
#     pdf.drawString(10,300, 'y300')
#     pdf.drawString(10,400, 'y400')
#     pdf.drawString(10,500, 'y500')
#     pdf.drawString(10,600, 'y600')
#     pdf.drawString(10,700, 'y700')
#     pdf.drawString(10,800, 'y800')
#
#
# filename = "testa.pdf"
#
# if os.path.exists(filename):
#     os.remove(filename)
#
# pdf = Canvas(f"static/{filename}")
#
#
#
# pdf.setTitle('invoice')
# pdf.drawImage("static/image.png",30,700, width=150,height=100)
# pdf.setFont("Helvetica-Bold",16)
# pdf.drawCentredString(520,800, "FAKTURA")
# pdf.setFont("Times-Roman",12)
# pdf.drawString(30,670, "namn")
# pdf.drawString(30,655, "adresse")
# pdf.drawString(30,640, "postkode, by")
# pdf.drawString(350,785, "------------------------------------------------------")
# pdf.drawString(350,770, "ConsultAS")
# pdf.drawString(350,755, "Adresse")
# pdf.drawString(350,740, "postkode, by")
# pdf.drawString(350,725, "------------------------------------------------------")
# pdf.setFont("Times-Roman",10)
# pdf.drawString(350,710, "Leveringsdato: ")
# pdf.drawString(350,695, "Levert til: ")
# pdf.setFont("Times-Roman",12)
# pdf.drawString(350,690, "------------------------------------------------------")
# pdf.drawString(350,675, "Fakturadato: ")
# pdf.drawString(350,660, "Fakturnr: ")
# pdf.drawString(350,645, "Forfallsdato: ")
# pdf.setFont("Helvetica-Bold",10)
# pdf.drawString(30,600, "BESKRIVELSE")
# pdf.drawString(300,600, "PRIS")
# pdf.drawString(375,600, "ANTALL")
# pdf.drawString(450,600, "MVA")
# pdf.drawString(525,600, "Beløp")
# pdf.setFont("Times-Roman",12)
# pdf.drawString(0,590, "----------------------------------------------------------------------------------------------")
# pdf.drawString(300,590, "-------------------------------------------------------------------------")
# pdf.drawString(30,575, "stor nettverkspakke ")
# pdf.drawString(30,545, "impletasjon av stor nettverkspakke ")
# pdf.drawString(300,575, "35000")
# pdf.drawString(300,545, "PRIS")
# pdf.drawString(375,575, "35")
# pdf.drawString(375,545, "PRIS")
# pdf.drawString(450,575, "25%")
# pdf.drawString(450,545, "25%")
# pdf.drawString(525,575, "Beløp")
# pdf.drawString(525,545, "35000")
# pdf.drawString(0,535, "----------------------------------------------------------------------------------------------")
# pdf.drawString(300,535, "-------------------------------------------------------------------------")
# pdf.setFont("Helvetica-Bold",10)
# pdf.drawString(30,520, "MVA-sats")
# pdf.drawString(115,520, "Grunnlag")
# pdf.drawString(200,520, "MVA")
# pdf.setFont("Times-Roman",10)
# pdf.drawString(30,505, "25%")
# pdf.drawString(115,505, "80000")
# pdf.drawString(200,505, "75000")
# pdf.drawString(290,520, "Nettobeløp:")
# pdf.drawString(290,505, "Meirverdiavgift:")
# pdf.drawString(525,520, "10000000")
# pdf.drawString(525,505, "100000")
# pdf.drawString(290,495, "-----------------------------------------------------------------------------------------")
# pdf.setFont("Helvetica-Bold",14)
# pdf.drawString(290,475, "Å BETALE")
# pdf.drawString(500,475, "600000")
# pdf.drawString(30,150, "BETALINGSINFORMAJON")
# pdf.setFont("Times-Roman",12)
# pdf.drawString(0,140, "----------------------------------------------------------------------------------------------")
# pdf.drawString(300,140, "-------------------------------------------------------------------------")
# pdf.setFont("Times-Roman",10)
# pdf.drawString(30,130, "Fakturanummer: ")
# pdf.drawString(30,115, "Sum å betale: ")
# pdf.drawString(300,130, "Bankonto: ")
#
#
# pdf.save()


import sqldb as t


#
# brukarinput= "1232"
#
# stmt = "SELECT * FROM tilsettinfo WHERE TilsettID = %s"
# cursor.execute(stmt, (brukarinput,))
# halla = cursor.fetchall()
#
# print(halla)
epost = "heidi@consultas.no"
ansattid = "1968"
passord = "1968"




# adduser = t.lagre_brukarinfo(ansattid,epost,passord)
# adduser.user()

# kunde_namn = "baffdsdsfdgfdltinn"
# kunde_epost = "bafdfsdlfdgdtinn@sales.no"
# kunde_adress = "vefsdsddfgn 3"
# kunde_by = "sogffdsdfsndal"
# kunde_postnr = "7875"
# tjeneste = "3"
# timer_brukt = "3"
# matrial = "5"
#
# send_til_db = t.Lagrefaktura(kunde_by, kunde_namn, kunde_epost, kunde_adress, kunde_postnr, timer_brukt,
#                              ansattid, matrial, tjeneste)
# send_til_db.kundepostnr()
# from sqldb import *
# faktura_id ="11"
#
# db = connect("faktura")
# cursor = db.cursor()
# cursor.execute("SELECT kunde.namn, kunde.Epost, kunde.Adresse, POSTKODE_PostNR, POSTNR.by_namn "
#                "FROM faktura "
#                "INNER JOIN kunde ON FAKTURA.KUNDE_ID = KUNDE.ID "
#                "INNER JOIN POSTNR ON KUNDE.POSTKODE_PostNR = POSTNR.Postkode "
#                "WHERE FAKTURA.ID = %s "
#                "GROUP BY FAKTURA.ID", (faktura_id,))
# kunde_info = cursor.fetchone()
# # hente ut seljar info
# cursor.execute("SELECT SELJAR.namn, SELJAR.Adresse, SELJAR.kontonummer, POSTKODE_PostNR, POSTNR.by_namn "
#                "FROM faktura "
#                "INNER JOIN SELJAR ON FAKTURA.SELJAR_ID = SELJAR.ID "
#                "INNER JOIN POSTNR ON SELJAR.POSTKODE_PostNR = POSTNR.Postkode "
#                "WHERE FAKTURA.ID = %s "
#                "GROUP BY FAKTURA.ID;", (faktura_id,))
# seljar_info = cursor.fetchone()
# print(seljar_info)
# # hente ut faktura info
# cursor.execute("select ID, Dato_betaling, Total_pris FROM FAKTURA WHERE ID = %s", (faktura_id,))
# faktura_info = cursor.fetchone()
# print(faktura_info)
# # hente ut jobbinfo
# cursor.execute("SELECT jobb.Timer_brukt, jobb.dato, TJENESTE.Namn, TJENESTE.Pris, MATRIAL.namn, MATRIAL.pris "
#                "FROM FAKTURA "
#                "INNER JOIN jobb ON FAKTURA.Jobb_ID = jobb.ID "
#                "INNER JOIN TJENESTE ON JOBB.TJENESTE_ID = TJENESTE.ID "
#                "INNER JOIN MATRIAL ON JOBB.MATRIAL_ID = TJENESTE.ID "
#                "WHERE FAKTURA.ID = %s "
#                "GROUP BY FAKTURA.ID;", (faktura_id,))
# jobbinfo = cursor.fetchone()
# print(jobbinfo)
# from createpdf import *
# db = connect("faktura")
# cursor = db.cursor()
# cursor.execute("SELECT ID FROM FAKTURA ORDER BY ID DESC LIMIT 1")
# faktura_id = cursor.fetchone()
# faktura_id = faktura_id[0]
# create_pdf(faktura_id)

# from argon2 import PasswordHasher, Type
# db = connect("innloggingsinformasjon")
# cursor = db.cursor(prepared=True)
# lagre_passord = ("INSERT INTO innloggingsinfo(TILSETTINFO_TilsettID, Epost, Passord) VALUES (%, %, %)")
# halla = input("skriv inn passord: ")
# epost = "karl@consultas.no"
# id = "2345"
#
# ph = PasswordHasher(
#     memory_cost=65636,
#     time_cost=4,
#     parallelism=2,
#     salt_len= 16,
#     hash_len=32,
#     type=Type.ID)
# passwordhash = ph.hash(halla)
#
#
# try:
#     id = ph.verify(passwordhash, "666")
#     if ph.check_needs_rehash(passwordhash):
#         ph = PasswordHasher(
#             memory_cost=65636,
#             time_cost=4,
#             parallelism=2,
#             salt_len=16,
#             hash_len=32,
#             type=Type.ID)
#         passwordhash = ph.hash(halla)
#     melding = "rett"
# except:
#     melding = "feil_passord"
#
#
# print(id)
#
# print(halla)

# passord = ("123456")
# brukerid ="1528"
bruker ="per@consultas.no"
# finne_bruker = "SELECT BrukerID, Epost, Passord FROM innloggingsinfo WHERE Epost = %s"
# cursor.execute(finne_bruker, (bruker,))
# user = cursor.fetchone()
# oppdater = "UPDATE innloggingsinfo SET Passord = %s WHERE TILSETTINFO_TilsettID =%s"
# cursor.execute(oppdater, (passord, brukerid,))
# db.commit()
# finne_bruker = "SELECT BrukerID, Epost, Passord FROM innloggingsinfo WHERE Epost = %s"
# cursor.execute(finne_bruker, (bruker, ))
# user = cursor.fetchone()
# db_passord = user[2]

# faktura_nummer = 2
# halla = os.path.exists(f"static/faktura{faktura_nummer}.pdf")
import os
# print(halla)
# with open('config', 'r') as f:
#     innhold = f.readlines()
#     user = innhold[0]
#
#
# print(user)
import re
password = "Z"
msg = "ikkjenoko"
if re.search("[A-Z]", password) is None:  # sjekke om passord inneholder store bokstaver
    msg = "Passordet må inneholde minst ein stor bokstav"

print(msg)