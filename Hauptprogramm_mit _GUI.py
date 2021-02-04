#Imports
import PySimpleGUI as sg 
from Dateihandle import search_data
from Dateihandle import get_data
from Dateihandle import save_data
from Dateihandle import delete_data
from Dateihandle import get_day
from Dateihandle import send_mail
from Dateihandle import show_mail
from Dateihandle import Kalenderwoche
from Dateihandle import suche_KW
from Dateihandle import get_highest_id
from Dateihandle import mail_body
from Dateihandle import text_for_mail_body
from Dateihandle import check_vacancy

import json

#Konfigurationsdatei
with open("data_file.json") as json_data_file:
    jdata = json.load(json_data_file)
#Zugriff Konfigurationsdatei
tab4=jdata["tab4"]

anfrage = [] #Tab4: Liste der Anfragen
hid = get_highest_id() #Tab4: Holt höchste ID aus Buchungsliste
choices =[] #Tab1: Liste der Listbox
header = ["ID  Wochentag Datum  Start  Ende  Person  Produktion  Art  Status"] #Tab2: Header für Table
mails = [] #Tab 2: Liste mit Buchungen 
raum =[]  #Tab 3: Liste mit Buchungen (Räume)

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
tab2_layout = [ [sg.Text('Hier können Sie die Buchungen nach Kalenderwoche und Jahr sehen:')],
            [sg.Text('Kalenderwoche:', size=(18,0)), sg.Text('Jahr:', size=(10,0)), sg.Text('Status:', size=(10,0))],   
            [sg.InputText(size=(20,10), key='KW'),sg.Drop(values = tab4["droplist_jahr"], key='Year', size=(10,10)) , sg.Drop(values = tab4["droplist_status"], key='status1', size=(10,10)), sg.Button('OK')],
            [sg.Listbox(mails,size=(100, 15),key='listbox2', enable_events=True)],
            #[sg.Text(key='e-mail body',size=(35, 10))], 
            [sg.Text('Sie können eine E-Mail mit der folgenden Buchungsliste senden' )],                         
            [sg.Button('Send mail'),sg.Button('Edit mail'), sg.Button('Clear')],
                ]  
#Tab3 - Raum Meldungen
#tab3_layout = [ [sg.Text('Hier können Sie Räume mit dem Status "unbearbeitet" anschauen. ')],
#            [sg.Text('Geben Sie bitte die Kalenderwoche und das Jahr ein. ')],
#            [sg.Text('Kalenderwoche:', size=(18,0)), sg.Text('Jahr:', size=(10,0))], 
#            [sg.InputText(size=(20,10), key='KW_1') ,sg.Drop(values = tab4["droplist_jahr1"], key='Year1', size=(10,10)) , sg.Button('Übernehmen')],
#           # [sg.Text('Gebuchte Räume für folgenden Woche :' )],
#            [sg.Listbox(mails,size=(100, 15),key='listbox3', enable_events=True)],
#            [sg.Button('Entfernen'), sg.Button('mail')],
#                ] 

#Tab4 - Eingabe
tab4_layout = [[sg.T('Hier können weitere Raumbuchungsanfragen erstellt werden.')],
               #[sg.Radio('Einfachanfragen     ', "anfrage1", default=True, size=(10,1)), sg.Radio('Mehrfachanfragen', "anfrage2")],
                
                #Infos zur Raumanfrage
                #Beschriftung:
                [sg.Text('Raumwunsch:', size=(19,0)), sg.Text('Datum:', size=(19,0)), sg.Text('Startzeit:', size=(19,0)),sg.Text('Endzeit:', size=(20,0))],
                [sg.Drop(values = tab4["droplist1"], key='raum', size=(20,200)),
                sg.Input(key='datum', size=(22,200)), sg.InputText(key='start', size=(22,200)),sg.InputText(key='ende', size=(22,200))],
                #Beschriftung
                [sg.Text('Verantwortlicher:', size=(19,0)), sg.Text('Produktion:', size=(19,0)), sg.Text('Veranstaltungsart:', size=(19,0)),sg.Text('Status:', size=(20,0))],
                [sg.InputText(key='person', size=(22,200)), sg.InputText(key = 'produkt', size=(22,200)),
                sg.Drop(values= tab4["droplist2"], key='art', size=(20,200)),
                sg.Drop(values = tab4["droplist3"], key='status', size=(20,200))],
                #popup frage
                [sg.B('Anfrage übernehmen', key= 'ueber')],
                [sg.Output(key = 'Output_Ein')],
                [sg.B('Anfrage(n) speichern', key = 'speichern')]]
            
# Gesamtes Layout und Fenster

#layout = [[sg.TabGroup([[sg.Tab('Suche', tab1_layout, tooltip='Toll'), sg.Tab('Wöchentliche Meldungen', 
 #       tab2_layout), sg.Tab('Raum Meldungen', tab3_layout), sg.Tab('Eingabe', tab4_layout)]], tooltip='Geil')] ]

# Gesamtes Layout und Fenster ohne Tab 3

layout = [[sg.TabGroup([[sg.Tab('Suche', tab1_layout, tooltip='Toll'), sg.Tab('Wöchentliche Meldungen', 
        tab2_layout), sg.Tab('Eingabe', tab4_layout)]], tooltip='Geil')] ]


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
    Jahr=values['Year']
    Status =['status1']
    #Tab3: Values zur Ausgabe
 #   K_W1=values['KW_1']
 #   Jahr_1=values['Year1']

#Tab1 - - - - -
    #Suchfunktion
    if event == 'Suchen':  
        window.FindElement('listbox').Update('')
        choices = search_data(textInputs_such) #Aufruf und Ausgabe der Suchfunktion
        window.FindElement('listbox').Update(header+choices)
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
    #Suche von Buchungen in Abhängigkeit von der  Kalenderwoche
    if event == 'OK':
        window.FindElement('listbox2').Update('')
        mails = mail_body(K_W,Jahr,Status)
        window.FindElement('listbox2').Update(mails)
    # Senden E-mail mit Buchungsliste (Abhängig von der  Kalenderwoche)
    if event == 'Send mail':
        send_mail(K_W,Jahr,Status)
    # Möglichkeit, E-Mails vor dem Senden zu korrigieren 
    if event == 'Edit mail':
        show_mail(K_W,Jahr,Status)
       # show_mail(header+K_W)
    #Leeren der Liste
    if event == 'Clear': 
        window.FindElement('listbox2').Update('')   
  
#Tab3 - - - - - 
    # Anzeige von gebuchten Räumen (Dautum + Zeit ) in Abhängigkeit  von der  Kalenderwoche
   # if event == 'Übernehmen':
    #    window.FindElement('listbox3').Update('')
     #   raum = raum_body(K_W1,Jahr_1)
      #  window.FindElement('listbox3').Update(raum)
    #Leeren der Liste
    #if event == 'Entfernen': 
    #    window.FindElement('listbox3').Update('') 
    #if event == 'mail': 
    #    show_mail(K_W1,Jahr_1,'y') 

#Tab4 - - - - -  
    #Eingabe neuer Eintrag
    if event == 'ueber':
        check = check_vacancy(in_raum, in_datum, in_start, in_ende)
        if check is not False : #Popup Warnung
            sg.popup("Raum schon belegt von:", check)
        else: #Speicherung in der Daten Templiste
            wtag = get_day(in_datum)
            hid = hid + 1 #höchste ID +1
            anfrage.append([hid,in_raum, wtag, in_datum, in_start, in_ende, in_person, in_produkt, in_art, in_status])
            print(hid, in_raum, wtag, in_datum, in_start, in_ende, in_person, in_produkt, in_art, in_status)
    #Speichern der Einträge
    if event == 'speichern': 
        save_data(data1 + anfrage)
        sg.popup("Anfragen gespeichert")
        anfrage = []

#Programm beenden - - - - -
    if event == sg.WIN_CLOSED: 
        break

window.close()