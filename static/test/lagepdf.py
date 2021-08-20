from sqldb import *
from reportlab.pdfgen.canvas import Canvas
import os
#starter med faktura id
def create_pdf(faktura_id):
    # hente ut kunde info
    db = connect("faktura")
    cursor = db.cursor()
    cursor.execute("SELECT kunde.namn, kunde.Epost, kunde.Adresse, POSTKODE_PostNR, POSTNR.by_namn "
                    "FROM faktura "
                    "INNER JOIN kunde ON FAKTURA.KUNDE_ID = KUNDE.ID "
                    "INNER JOIN POSTNR ON KUNDE.POSTKODE_PostNR = POSTNR.Postkode "
                    "WHERE FAKTURA.ID = %s "
                    "GROUP BY FAKTURA.ID", (faktura_id,))
    kunde_info = cursor.fetchone()
    # hente ut seljar info
    cursor.execute("SELECT SELJAR.namn, SELJAR.Adresse, SELJAR.kontonummer, POSTKODE_PostNR, POSTNR.by_namn "
                    "FROM faktura "
                    "INNER JOIN SELJAR ON FAKTURA.SELJAR_ID = SELJAR.ID "
                    "INNER JOIN POSTNR ON SELJAR.POSTKODE_PostNR = POSTNR.Postkode "
                    "WHERE FAKTURA.ID = %s "
                    "GROUP BY FAKTURA.ID;", (faktura_id,))
    seljar_info = cursor.fetchone()
    # hente ut faktura info
    cursor.execute("select ID, Dato_betaling, Total_pris FROM FAKTURA WHERE ID = %s",(faktura_id,))
    faktura_info = cursor.fetchone()

    # hente ut jobbinfo
    cursor.execute("SELECT jobb.Timer_brukt, jobb.dato, TJENESTE.Namn, TJENESTE.Pris, MATRIAL.namn, MATRIAL.pris "
                    "FROM FAKTURA "
                    "INNER JOIN jobb ON FAKTURA.Jobb_ID = jobb.ID "
                    "INNER JOIN TJENESTE ON JOBB.TJENESTE_ID = TJENESTE.ID "
                    "INNER JOIN MATRIAL ON JOBB.MATRIAL_ID = TJENESTE.ID "
                    "WHERE FAKTURA.ID = %s "
                    "GROUP BY FAKTURA.ID;", (faktura_id,))
    jobbinfo = cursor.fetchone()


    kunde_namn = kunde_info[0]
    kunde_epost= kunde_info[1]
    kunde_adresse= kunde_info[2]
    kunde_postkode= kunde_info[3]
    kunde_by= kunde_info[4]
    seljar_namn=seljar_info[0]
    seljar_adresse= seljar_info[1]
    seljar_konto= seljar_info[2]
    seljar_poskode=seljar_info[3]
    seljar_by = seljar_info[4]
    fakturaid= faktura_info[0]
    betalingsdato = faktura_info[1]
    totalpris = faktura_info[2]
    timer_brukt = jobbinfo[0]
    dato_opretta = jobbinfo[1]
    tjeneste_namn= jobbinfo[2]
    tjeneste_pris = jobbinfo[3]
    matrial_namn = jobbinfo[4]
    matrial_pris = jobbinfo[5]
    totalpris_tjeneste= int(tjeneste_pris)*int(timer_brukt)
    nettopris = totalpris/(1.25)
    mva = totalpris-nettopris

    filename = f"static/Faktura{faktura_id}.pdf"

    if os.path.exists(filename):
        return "det er allerede opretta en faktura for denne"

    pdf = Canvas(filename)

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
    pdf.drawString(350, 740, f"{str(seljar_poskode)} {seljar_by}")
    pdf.drawString(350, 725, "------------------------------------------------------")
    pdf.setFont("Times-Roman", 10)
    pdf.drawString(350, 710, f"Leveringsdato: {str(dato_opretta)}")
    pdf.drawString(350, 695, f"Levert til: {kunde_adresse}, {kunde_postkode}, {kunde_by}")
    pdf.setFont("Times-Roman", 12)
    pdf.drawString(350, 690, "------------------------------------------------------")
    pdf.drawString(350, 675, f"Fakturadato: {str(dato_opretta)}")
    pdf.drawString(350, 660, f"Fakturnr: {str(fakturaid)}")
    pdf.drawString(350, 645, f"Forfallsdato: {str(betalingsdato)}")
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

    pdf.save()



#hente ut seljar info

#hente ut faktura info

#hente ut jobbinfo

# hente ut