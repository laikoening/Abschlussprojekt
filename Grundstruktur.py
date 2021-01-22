#Das soll das Grundkonzept werden

#IMPORTS
import os
import csv
import time
import datetime
from datetime import date
#für mehrdimensionale arrays
import numpy as np
#typische zeitfunktion
print(datetime.datetime.now().strftime("%A %b %w %H:%M:%S - %d.%m.%Y"))

#Daten aus Datei laden
def get_data():
    #Reader zum Öffnen der CSV Datei
    with open("C:/Users/kairu/OneDrive/7.Semester/Abschlussprojekt/rbl.csv") as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        header_row = next(reader)
        buchung = []

        #Schleife zum Einlesen der Daten
        for row in reader:
            buchung.append(row)
        #print(buchung)
        #zurückgeben von Buchung
        return buchung

#Eingabe neuer Daten
def input_data():

    quest = "nein"
    while True:
        #Eingabe Raum
        raum = input("Wählen Sie einen Raum")

        #Datumseingabe -> müsst auch schöner werden
        dd = input("Geben Sie den Tag ein:")
        mm = input("Geben Sie den Monat ein:")
        jj = input("Geben Sie das Jahr ein:")
        datum = date(int(jj), int(mm), int(dd)) 
        print(datum.strftime("%d.%m.%Y")) #Kalenderdatum mit bestimmten Format ausgeben
        print(datum.strftime("%A")) #Wochentag des Datums ausgeben

        """
        #Start und Endzeit eingeben
        starth = input("Geben Sie die Startstunde an:")
        startm = input("Geben Sie die Startminuten an:")
        startt = time(int(startm, int(startm)))
        print(startt)
        """

        if quest == "nein":
            1#Gleiche Angaben
            #person = input("Geben Sie den Verantwortlichen an:") 
            #produktion = input("Geben Sie die Produktion an:")  # dropdown liste
            #nutzung = input("Geben Sie die Nutzungsart an:")    #dropdown list
            #status = input("Geben Sie den Status an:")


        quest = input ("Sie wollen Sie eine Mehrfacheingabe starten?: [ja] [nein]")

        #Speicherung der Daten in CSV Datei
        with open('C:/Users/kairu/OneDrive/7.Semester/Abschlussprojekt/rbl.csv', mode='w') as csv_file:
            fieldnames = ['ID', 'Raum', 'Wochentag', 'Datum', 'Start', 'Ende', 'Verantwortliche', 'Produktion', 'Nutzungsart','Status']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')

            writer.writerow({'ID': '2', 'Raum': raum, 'Wochentag': datum.strftime("%A"), 'Datum': datum, 'Start': '20:00', 'Ende': '22:00', 'Verantwortliche': 'Kai Loening', 'Produktion': 'Erlenkoenig', 'Nutzungsart': 'Probe', 'Status': 'bestaetigt'})
            #immer mit ';' trennen, um einzelne Kästchen zu beschreiben
        break

#def check_data():

#Anzeige der Raumbuchungsdaten
def view_data():
    view = get_data()
    #Zeilenweise ausgeben der Buchungen
    for i in view:
        print(i)

def search_data():

    buchung = get_data()
    while True:
        auswahl1 = input("Nach was wollen sie suchen? \n[1] Verantwortlichen \n[a]abbrechen\n")

        #Suche nach Verantwortlichen
        if auswahl1 == "1":
            name = input("Geben Sie den Namen des Verantwortlichen ein:")
            i = 0
            liste = [] #Liste der gefunden passenden Buchungen
            while i < len(buchung): #Beginn Suchalgorythmus
                if buchung[i][6] == name:
                    liste.append(buchung[i])
                i = i+1
            for l in liste: #Zeilenweise ausgabe der gefundenen Daten
                print(l)

            #Anfrage für Löschung des Daten

    
        if auswahl1 == "a":
            break

#def delete_data():

#def archive_data():

#def show_warnings():

#def mail_raummeldungen():

#def mail_wochenmeldung():


#Programmablauf
while True: 
    auswahl = input("Wählen Sie eine Option: \n[1] neue Buchung(en) \n[2] Anzeige der Buchungsliste \n[4] Suche nach Daten \n[a] Abbrechen\n")
    if auswahl == "1":
        input_data()
    if auswahl == "2":
        view_data()
    if auswahl == "3":
        get_data()
    if auswahl == "4":
        search_data()
    if auswahl == "a":
        break
    print("hallo")
