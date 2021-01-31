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

#def prove_data():

#def archive_data():

#def show_warnings():


#Lenas Funktonen

def Kalenderwoche():
    data=get_data()
    x=[]
    liste={}
    for value in data:
        day, month, year = (int(n) for n in value[3].split('.'))
        X_Woche = datetime.date(year, month, day)   
        week_number = X_Woche.isocalendar()[1] 
        liste[week_number]=value[0:9] 
    for key,value in liste.items(): 
        temp= [key,value]
        x.append(temp)       
        #liste.append(value[0:9])
        #liste.insert(10,week_number)
        #print(liste)
        #if KW in liste.keys():
    #print(x)
    return(x)
        #else:
         #   err='no data'
          #  return(err)
        #return(x)
def suche_KW(KW):
    KW = int(KW)
    liste=Kalenderwoche() 
    x=[]
    i=0
    while i<len(liste):
        if liste[i][0]==KW:
            x.append(liste[i][1:9])
        i=i+1
    return(x)


def send_mail():
       
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)                           # outlook MailItem == 0
    mail.To = 'olena.pokotilova@gmail.com'
    mail.Subject = 'Message subjeact'       
    mail.Body = 'Message body'                             # take text from "Buchungsliste"
    mail.Send()

#E-Mail anschauen   
def show_mail(KW):
    text = suche_KW(KW)
    print(text)
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)                           # outlook MailItem == 0
    mail.To = 'olena.pokotilova@gmail.com'
    mail.Subject = 'Message subject'       
    #mail.Body = '\n'.join(text)   # take text from "Buchungsliste" 
    #body = '\n'.join('%s, %s' % pair for pair in mylist)
   # mail.Body = "  ".join(text[0][0])
    mail.Body = "Sehr geeherte Frau Wußler,\n Unsere geplanten Veranstaltungen für die nächsten Woche sind die Folgenden: \n #{2}, {3} \n {4} - {5} Uhr , {8} \n MfG \n Kai Löning ".format(*text[0][0])
    mail.Display(True)                                     # show and edit mail 
    





#while True:
   # action= input('test')
    #if action== 't':
        #message_body()
       # show_mail(3)
    #show_mail()