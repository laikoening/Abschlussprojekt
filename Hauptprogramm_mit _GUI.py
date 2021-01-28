#Imports
import PySimpleGUI as sg 
from Dateihandle import search_data
from Dateihandle import get_data
from Dateihandle import save_data
from Dateihandle import delete_data
from Dateihandle import send_mail
from Dateihandle import show_mail
from Dateihandle import Kalenderwoche

import json

#Konfigurationsdatei
with open("data_file.json") as json_data_file:
    jdata = json.load(json_data_file)
#Zugriff Konfigurationsdatei
tab4=jdata["tab4"]

anfrage = [] #Tab4: Liste der Anfragen
choices =[] #Tab1: Liste der Listbox
mails = [] #Tab 2: Liste mit Buchungen 

#Design des Fenstern
#sg.theme_previewer() #show all themes
sg.theme('Topanga') #choose a theme

#Tab1 - Suche
tab1_layout = [[sg.Text('Geben Sie einen Suchbegriff ein:')], 
 [sg.InputText(size=(20,10), key='Input'), sg.B('Suchen')], 
 #[sg.Output(key = 'Output')],
 [sg.Listbox(choices,size=(100, 20),key='listbox', enable_events=True)],
 [sg.B('Alle Anzeigen'),sg.B('Eintrag Löschen'), sg.B('Liste Leeren'),sg.B('Infobox')]]

#Tab2 - Wöchentliche Meldungen
tab2_layout = [ [sg.Text('Geben Sie die Kalenderwoche ein:')],
            [sg.InputText(size=(20,10), key='KW'), sg.Button('OK')],
            [sg.Listbox(mails,size=(100, 20),key='listbox2', enable_events=True)],
            [sg.Text(key='e-mail body',size=(35, 10))],                          
            [sg.Button('Send mail'),sg.Button('Edit mail'), sg.Button('Exit')],
                ]  
#Tab3 - Raum Meldungen
tab3_layout = [[sg.T('Hier arbeitet Olena gerade dran.')]] 

#Tab4 - Eingabe
tab4_layout = [[sg.T('Hier können weitere Raumbuchungsanfragen erstellt werden.')],
               #[sg.Radio('Einfachanfragen     ', "anfrage1", default=True, size=(10,1)), sg.Radio('Mehrfachanfragen', "anfrage2")],
                
                #Infos zur Raumanfrage
                [sg.Drop(values = tab4["droplist1"], key='raum', size=(20,200)),
                sg.Input('Datum',key='datum', size=(22,200)), sg.InputText(key='start', size=(22,200)),sg.InputText(key='ende', size=(22,200))],
                [sg.InputText(key='person', size=(22,200)), sg.InputText(key = 'produkt', size=(22,200)),
                sg.Drop(values= tab4["droplist2"], key='art', size=(20,200)),
                sg.Drop(values = tab4["droplist3"], key='status', size=(20,200))],
                
                [sg.B('Anfrage übernehmen', key= 'ueber')],
                [sg.Output(key = 'Output_Ein')],
                [sg.B('Anfrage(n) speichern', key = 'speichern')]]
            
# Gesamtes Layout und Fenster
layout = [[sg.TabGroup([[sg.Tab('Suche', tab1_layout, tooltip='Toll'), sg.Tab('Wöchentliche Meldungen', 
        tab2_layout), sg.Tab('Raum Meldungen', tab3_layout), sg.Tab('Eingabe', tab4_layout)]], tooltip='Geil')] ]

window = sg.Window('DIE BÜHNE', layout, default_element_size=(100,20)) #create a window

# Event Loop to process "events" and get the "values" of the inputs
while True: 
    data1 = get_data() #Tab4

    event, values = window.read() 
    textInputs_such = values['Input']
    #Tab4: Values zur Ausgabe
    in_raum = values['raum']
    in_datum = values['datum']
    in_start = values['start']
    in_ende = values['ende']
    in_person = values['person']
    in_produkt = values['produkt']
    in_art = values['art']
    in_status = values['status']

    #Tab2: Values zur Ausgabe
    K_W=values['KW']

#Tab1 - - - - -
    #Suchfunktion
    if event == 'Suchen':  
        window.FindElement('listbox').Update('')
        choices = search_data(textInputs_such) #Aufruf und Ausgabe der Suchfunktion
        window.FindElement('listbox').Update(choices)
    #Anzeigen aller Einträge    
    if event == 'Alle Anzeigen': 
        window.FindElement('listbox').Update('')
        choices = get_data()
        window.FindElement('listbox').Update(choices)
    #Löschen des ausgewählten Elements
    if event == 'Eintrag Löschen': 
        get = values['listbox'][0] #hier muss das Listenelement erst umgewandelt werden
        do = get[0]
        delete_data(do)
        #liste aktualisieren
        choices = search_data(textInputs_such)
        window.FindElement('listbox').Update(choices)
    if event == 'Infobox': 
        sg.popup("DIE BÜHNE - das Theater der TU Dresden")
    #Leeren der Liste
    if event == 'Liste Leeren': 
        window.FindElement('listbox').Update('')
#Tab2 - - - - -  
    if event == 'OK':
        window.FindElement('listbox2').Update('')
        mails = Kalenderwoche(K_W)
        window.FindElement('listbox2').Update(mails)
    if event == 'Send mail':
        send_mail()
    if event == 'Edit mail':
        show_mail()
    if event == 'Exit':
        window.Close()

#Tab4 - - - - -  
    #Eingabe neuer Eintrag
    if event == 'ueber':
        anfrage.append(["2",in_raum,"Freitag", in_datum, in_start, in_ende, in_person, in_produkt, in_art, in_status])
        print(in_raum, in_datum, in_start, in_ende, in_person, in_produkt, in_art, in_status)
    #Speichern der Einträge
    if event == 'speichern': 
        save_data(data1 + anfrage)
        sg.popup("Anfragen gespeichert")
        anfrage = []
#Programm beenden - - - - -
    if event == sg.WIN_CLOSED: 
        break

window.close()