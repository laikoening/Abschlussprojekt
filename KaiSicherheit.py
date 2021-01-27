#Status 26.01., bitte nicht ändern!



# ------- IMPORTS -------
import os
import csv
import time
import datetime
from datetime import date
#Konfigurationstool
import configparser
#für mehrdimensionale arrays
import numpy as np
#typische zeitfunktion
print(datetime.datetime.now().strftime("%A %b %w %H:%M:%S - %d.%m.%Y"))

# ------- Konfigurationsdatei -------
with open('confi.ini', 'r') as configfile:
    config = configparser.ConfigParser()
    config.read("confi.ini")
#Zugriff Konfigurationsdatei
settings = config["settings"]

#-------Daten aus Datei laden-------
def get_data():
    #Reader zum Öffnen der CSV Datei
    #valid = False
    pfad = settings["Buchungspfad"] # macht wenig Sinn den Pfad hier stehen zu haben
    while True:
        try:
            with open(pfad) as csv_file:
                reader = csv.reader(csv_file, delimiter=';')
                #header_row = next(reader)
                data_get = []
                
                    #Schleife zum Einlesen der Daten
                for row in reader:
                    data_get.append(row)
                #print(buchung)
                #zurückgeben von Buchung
            return data_get
        except:
            print("Datei nicht gefunden!\n")
            print("Bisheriger Pfad:", pfad)
            pfad = input("Bitte geben sie einen gültigen Pfad ein:")

#------- Eingabe neuer Daten -------
def input_data():
    data_in = get_data()
    quest1 = "Ja"
    while True:
        #Vergabe ID
        id = 2
        #Eingabe Raum
        raum = input("Wählen Sie einen Raum")

        #Datumseingabe -> müsst auch schöner werden
        dd = input("Geben Sie den Tag ein:")
        mm = input("Geben Sie den Monat ein:")
        jj = input("Geben Sie das Jahr ein:")
        datum = date(int(jj), int(mm), int(dd)) 
        tag = datum.strftime("%A")

        print(datum.strftime("%d.%m.%Y")) #Kalenderdatum mit bestimmten Format ausgeben
        print(datum.strftime("%A")) #Wochentag des Datums ausgeben
        
        #Start und Endzeit eingeben
        starth = input("Geben Sie die Startstunde an:")
        startm = input("Geben Sie die Startminuten an:")
        #startt = time(int(startm), int(startm))
        start = 20
        #print(startt)
        endt = 22
        
        #Gleiche Angaben
        if quest1 == "nein":
            person = input("Geben Sie den Verantwortlichen an:") 
            produktion = input("Geben Sie die Produktion an:")  # dropdown liste
            nutzung = input("Geben Sie die Nutzungsart an:")    #dropdown list
            status = input("Geben Sie den Status an:")  #dropdown list

        #in zwischenliste ablegen
        buchungtemp =[id, raum, tag, datum, start, endt, person, produktion, nutzung, status]
        data_in.append(buchungtemp)
        print(buchungtemp)
        
        quest1 = input ("Sie wollen Sie eine Mehrfacheingabe starten?: [ja] [nein]") #Frage, ob Daten gleich bleiben sollen
        quest2 = input("Wollen Sie weitere Eingaben vornehmen?")


        if quest1 and quest2 == "nein":
            #Speicherung der Daten in CSV Datei und Programmende
            save_data(data_in)
            break

# ------- Daten speichern ------- 
def save_data(data_sa):
    print(data_sa)
    valid = False 
    pfad  = settings["Buchungspfad"]
    while not valid:
        try:
            with open(pfad, mode='w', newline='') as csv_file:
                    writer = csv.writer(csv_file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                    writer.writerows(data_sa)
                    print("Buchungsdaten gespeichert!")
                    valid = True
        except:
            print("Datei konnte nicht gefunden werden oder nicht gespeichert werden.")
            print("Bisheriger Pfad:", pfad)
            pfad = input("Bitte geben sie einen gültigen Pfad ein:")

#def check_data():

# ------- Anzeige der Raumbuchungsdaten -------
def view_data():
    view = get_data()
    #Zeilenweise ausgeben der Buchungen
    for i in view:
        print(i)

def search_data():

    data = get_data()
    print (data)
    while True:
        auswahl1 = input("Nach was wollen sie suchen? \n[1] Allgemeine Suche \n[a]abbrechen\n")

        #Allgemeine Suche
        if auswahl1 == "1":
            search = input("Geben Sie einen Suchbegriff ein:")
            i = 0
            liste = [] #Liste der gefunden passenden Buchungen
            while i < len(data): #Beginn Suchalgorythmus
                j=0
                while j < 9:
                    if data[i][j] == search:
                        print(data[i][j])
                        liste.append(data[i])
                    j = j +1
                i = i+1
            if not liste:
                print("keine Treffer!")
                return

            #Zeilenweise ausgabe der gefundenen Daten    
            for l in liste: 
                print(l)
            return 
        #Abbruch der Anfrage
        if auswahl1 == "a":
            break

#  ------- löschen von Daten -------
def delete_data():
    data_de = get_data()
    search_data() #Aufruf der Suchfunktion, um Daten anzeigen zu lassen
    delete = input("Geben Sie die ID zum Löschen der Buchung ein:\n") #Suchvariable
    i = 0
    j = len(data_de)
    while i < j:
        if data_de[i][0] == delete:
            data_de.remove(data_de[i])
            print("Daten gelöscht!")
            break
        i = i+1
    save_data(data_de) #Speicherung der Daten 

#def archive_data():

#def show_warnings():

#def mail_raummeldungen():

# ------- Wöchentliche Meldungen -------
#def mail_wochenmeldung():

def mail_wochenmeldung():
    data=get_data()
    for value in data:
        day, month, year = (int(i) for i in value[3].split('.')) 
        KW = datetime.date(year, month, day)
        value.insert(10,KW.strftime("%V"))
        #print(KW.strftime("%V")) 
    #save_data(data)
    
        #print((KW))

def message_body():
    data=get_data()
    liste = {} 
    i=0
    while i< len(data):
        for value in data:
            key=value[2]
            liste[key] = value[4]+";"+value[5]
        if  data == None:
            print("no data")
        i=i+1
    print(liste) 


# ------- Programmablauf -------

while True: 
    auswahl = input("Wählen Sie eine Option: \n[1] neue Buchung(en) \n[2] Anzeige der Buchungsliste \n[4] Suche nach Daten \n[5] Löschen von Daten \n[a] Abbrechen\n")
    if auswahl == "1":
        input_data()
    if auswahl == "2":
        view_data()
    if auswahl == "3":
        buchung = get_data()
    if auswahl == "4":
        search_data()
    if auswahl == "5":
        delete_data()
    if auswahl == "a":
        break


