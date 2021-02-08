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
    data = get_data()
    liste = []
    for value in data:
        try:
            day, month, year = (int(n) for n in value[3].split('.'))
            X_Woche = datetime.date(year, month, day) 
            week_number = X_Woche.isocalendar()[1] 
            x = [week_number, year, value]
            liste.append(x) 
        except:
            print("Fehlerhafter Eintrag!")          
    return liste
 
# ------- Suche nach Kalenderwoche  -------

def suche_KW(KW, jahr):
    liste = kalenderwoche() 
    if len(liste) == 0:
            return ["Keine Treffer!"]
    x = []
    for row in liste:
        if row[0] == KW and row[1] == jahr:
            x.append(row[2])

    return x

# ------- Text für E-Mail (Wochentliche Meldung) -------

def data_for_mail_body (KW, jahr, status):
    data = suche_KW(KW, jahr)
    liste = []
    for row in data:
        if status == '':
            liste.append(row)
        elif status == row[9]:
            liste.append(row)

    return liste
  

def sort_by_datetime(row):
    day, month, year = (int(n) for n in row[3].split('.'))
    return datetime.date(year, month, day)


def mail_body(KW, jahr, status):
    try:
        KW = int(KW)
        jahr = int(jahr)
    except ValueError:
        return ["Parameter inkorrekt!"]
    data = data_for_mail_body(KW, jahr, status)
    if len(data) == 0:
        return ["Keine Treffer!"]
    data.sort(key=sort_by_datetime)
    liste = []
    for row in data:
        #body = "\n Raum: {1} , \n Datum : {2}, {3} \n Uhrzeit: {4} - {5} Uhr  ".format(*text[i])
        body = "\n #{2}, {3} \n {4} - {5} Uhr , {8} ".format(*row)
        liste.append(body)

    return liste



#------- Liste mit gebuchten Räumen -------
#def raum_body (KW,Jahr):
 #   text = suche_KW(KW,Jahr)
  #  i=0
   # liste=[]
    #while i<len(text):
     #   if text[i][0][9] == 'unbearbeitet':    
      #      body = "\n Raum: {1} , \n Datum : {2}, {3} \n Uhrzeit: {4} - {5} Uhr  ".format(*text[i][0])
       #     liste.append(body)
       # else:
        #    err ="keine Treffer!"
         #   return(err)
        #i=i+1    
    #return(liste)
    #print(liste)

#------- E-Mail mit Buchungsliste (Abhängig von der  Kalenderwoche) senden -------

def send_mail(KW, Jahr, Status, send):
    x=mail_body(KW,Jahr,Status)
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)                           # outlook MailItem == 0
    mail.To = 'olena.pokotilova@gmail.com'
    mail.Subject = 'Veranstaltungen für die nächsten Woche' 
    mail.Body = " Sehr geeherte Frau Wußler,\n Unsere geplanten Veranstaltungen für die nächsten Woche sind die Folgenden: " + " ".join(x) + "\n LG \n Kai Löning"
    if send:
        mail.Send()
    else:
        mail.Display(True)

#------- E-Mail mit Buchungsliste (Abhängig von der  Kalenderwoche) vor dem Senden anschauen  -------
# def show_mail(KW,Jahr,Status):
#     x=mail_body(KW,Jahr,Status)
#     outlook = win32.Dispatch('outlook.application')
#     mail = outlook.CreateItem(0)                           # outlook MailItem == 0
#     mail.To = 'olena.pokotilova@gmail.com'
#     mail.Subject = 'Veranstaltungen für die nächsten Woche' 
#     mail.Body = "Sehr geeherte Frau Wußler,\n Unsere geplanten Veranstaltungen für die nächsten Woche sind die Folgenden: " + " ".join(x) + "\n LG \n Kai Löning"  
#     mail.Display(True)                                   # show and edit mail

    



#while True:
 #   action= input('test')
 #   if action== 't':
        #print(Kalenderwoche())
        #suche_KW(43, 2020)
 #       mail_body2(43, 2020, "unbearbeitet")
        #Kalenderwoche()