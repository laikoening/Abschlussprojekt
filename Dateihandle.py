#Diese Datei dient zum Dateihandle

# ------- IMPORTS -------
import os
import csv
import time
import datetime
from datetime import date
import numpy as np #für mehrdimensionale arrays
import configparser
import json
import win32com.client as win32

# ------- Konfigurationsdatei -------
with open("data_file.json") as json_data_file:
    jdata = json.load(json_data_file)
#Zugriff Konfigurationsdatei
settings = jdata["settings"]

#-------Daten aus Datei laden-------
def get_data():
    #Reader zum Öffnen der CSV Datei
    #valid = False
    pfad = settings["buchungspfad"] # macht wenig Sinn den Pfad hier stehen zu haben
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

# ------- Daten speichern ------- 
def save_data(data_sa):
    valid = False 
    pfad  = settings["buchungspfad"]
    while not valid:
        try:
            with open(pfad, mode='w', newline='') as csv_file:
                    writer = csv.writer(csv_file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                    writer.writerows(data_sa)
                    valid = True
        except:
            print("Datei konnte nicht gefunden werden oder nicht gespeichert werden.")
            print("Bisheriger Pfad:", pfad)
            pfad = input("Bitte geben sie einen gültigen Pfad ein:")

# ------- Suche für die GUI -------
def search_data(search):

    data = get_data()          
    i = 0
    liste = [] #Liste der gefunden passenden Buchungen
    while i < len(data): #Beginn Suchalgorythmus
        j=0
        while j < 9:
            if data[i][j] == search:
                liste.append(data[i])
            j = j +1
        i = i+1
    if not liste:
        e = "keine Treffer!"
        return e
    #Zeilenweise ausgabe der gefundenen Daten    
    return liste  

#  ------- löschen von Daten -------
def delete_data(delete):
    data_de = get_data()
    i = 0
    j = len(data_de)
    while i < j:
        if data_de[i][0] == delete:
            data_de.remove(data_de[i])
            break
        i = i+1
    save_data(data_de) #Speicherung der Daten 

# ------- Wochentag ermitteln -------
def get_day(tag):
    tag = datetime.datetime.strptime(tag, '%d.%m.%Y')
    return tag.strftime('%A')

# -------- ID Erstellen -------
def get_highest_id():
    data_cr = get_data()
    i = 0
    id = 0
    while i < len(data_cr):
        if int(data_cr[i][0]) >= id: 
            id = int(data_cr[i][0]) #neue ID wird erst im Haupprogramm erstellt
        i = i + 1
    return id #gitb die höchste ID zurück

# ------- Zeitraum überprüfen -------
def check_vacancy(in_raum, in_datum, in_start, in_ende):
    data_va = get_data()
    i = 0
    while i < len(data_va):
        if data_va[i][3] == in_datum: #Verglich Datum
            if data_va[i][1] == in_raum: #Vergleich Raum
                #Umwanldung der String in Time
                ein_start = time.strptime(in_start, "%H:%M") #Startzeit Eingabe
                ein_ende = time.strptime(in_ende, "%H:%M") #Endzeit Eingabe
                tab_start= time.strptime(data_va[i][4], "%H:%M") #Startzeit Tabelle
                tab_ende = time.strptime(data_va[i][5], "%H:%M") #Endzeit Tabelle
                if (ein_ende < tab_ende) and (tab_start < ein_ende): #Zeitraum kleiner und/oder mittendrin
                    return data_va[i] #Schleifenende und Rückgabe des Tabelleneintrags 
                elif (ein_start < tab_ende) and (ein_start > tab_start): #größter und mittendrin 
                    return data_va[i]
                elif (ein_start < tab_start) and (ein_ende > tab_ende): #einrahmend
                    return data_va[i]
        i = i +1
    return False

#def archive_data():

#def show_warnings():

# ------- Kalenderwoche ermitteln -------

def kalenderwoche():
    data = get_data()                                                   # Diese Variable ist eine Liste
    liste = []
    for value in data:
        try:
            day, month, year = (int(n) for n in value[3].split('.'))    # Aufteilung des Datums(int) in day, month, year
            X_Woche = datetime.date(year, month, day)                   # Erstellung eines Datumsobjektes (datetime object)
            week_number = X_Woche.isocalendar()[1]                      # Return Kalenderwoche 
            x = [week_number, year, value]                              # Zusammenfassung der Kalenderwoche mit entsprechendem Jahr und Datensatz
            liste.append(x) 
        except:
            print("Fehlerhafter Eintrag!")                              # Fehlermeldung, wenn das Datum in .scv-Datei inkorrekt ist
    
    return liste
 
# ------- Suche nach Kalenderwoche  -------

def search_KW(KW, jahr):
    liste = kalenderwoche()                                             # Diese Variable ist eine Liste
    if len(liste) == 0:
            return ["Keine Treffer!"]
    x = []
    for row in liste:                                                   # Suche nach bestimmten Datensetz in Abhängigkeit von der Kalenderwoche und Jahr 
        if row[0] == KW and row[1] == jahr:
            x.append(row[2])

    return x

# ------- Data für E-Mail (Wochentliche Meldung) -------

def data_for_mail_body (KW, jahr, status):
    data = search_KW(KW, jahr)                                          # Diese Variable ist eine Liste
    liste = []
    for row in data:                                                    # Suche nach bestimmten Datensetz in Abhängigkeit vom Status
        if status == '':
            liste.append(row)
        elif status == row[9]:
            liste.append(row)

    return liste
  
# ------- Datum Sortieren  -------

def sort_by_datetime(row):                                              # Das Datum in aufsteigender Reihenfolge sortieren 
    day, month, year = (int(n) for n in row[3].split('.'))              # Aufteilung des Datums(int) in day, month, year
    return datetime.date(year, month, day)                              # Return datetime object

# ------- Text für E-Mail ---------

def mail_body(KW, jahr, status):
    try:                                                                # Prüfen ob die Eigaben valid sind
        KW = int(KW)                                                     
        jahr = int(jahr)
    except ValueError:
        return ["Parameter inkorrekt!"]
    data = data_for_mail_body(KW, jahr, status)                         # Diese Variable ist eine Liste
    if len(data) == 0:
        return ["Keine Treffer!"]
    data.sort(key=sort_by_datetime)                                     # Das Datum in aufsteigender Reihenfolge sortieren 
    liste = []
    for row in data:

        #body = "\n Raum: {1} , \n Datum : {2}, {3} \n Uhrzeit: {4} - {5} Uhr  ".format(*text[i])       # Text-Format_1 für mail body

        body = "\n #{2}, {3} \n {4} - {5} Uhr , {8} ".format(*row)      # Text-Format_2 für mail body  
        liste.append(body)

    return liste

def send_mail(KW, jahr, status, send):
    x=mail_body(KW, jahr, status)                                       # Diese Variable ist eine Liste
    # win32.client bietet Unterstützung für COM-Clients (z. B. Microsoft Excel, Outlook....). 
    # Die COM-Client-Unterstützung ermöglicht Python, andere COM-Objekte über ihre über ihre öffentlichen Schnittstellen bearbeiten.
    outlook = win32.Dispatch('outlook.application')        
    mail = outlook.CreateItem(0)                                        # outlook MailItem == 0
    mail.To = 'olena.pokotilova@gmail.com'
    mail.Subject = 'Veranstaltungen für die nächsten Woche' 
    mail.Body = "Sehr geeherte Frau Wußler,\nUnsere geplanten Veranstaltungen für die nächsten Woche sind die Folgenden: " + " ".join(x) + "\nLG \nKai Löning"
    if send:
        mail.Send()
    else:
        mail.Display(True)



