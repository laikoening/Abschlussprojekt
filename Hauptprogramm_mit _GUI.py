import PySimpleGUI as sg 
from Grundstruktur import search_data1
from Grundstruktur import get_data
from Grundstruktur import save_data

#Für die Eingabe Funktion
data1 = get_data()
anfrage = []



#sg.theme_previewer() #show all themes
sg.theme('Topanga') #choose a theme

#für die Dropdownlist der Eingabe
list1 = ['-Raumwunsch-','Buehne','KLEM','155','136']
list2 = ['-Veranstaltungsart-','Aufführung','Auswahlworkshop','Improtheater','Probe','Workshop', 'Sonstiges']
list3 = ['anfragen','ausstehend','bestätigt']

#Tab1 - Suche
tab1_layout = [[sg.Text('Geben Sie einen Suchbegriff ein:')], 
 [sg.InputText(size=(20,200), key='Input'), sg.B('Suchen')], 
 [sg.Output(key = 'Output')],
 [sg.B('Eintrag Löschen'), sg.B('Liste Leeren'),sg.B('Infobox')]]

#Tab2 - Wöchentliche Meldungen
tab2_layout = [[sg.T('This is inside tab 2')],    
               [sg.In(key='wochenmeldungen')]]  
#Tab3 - Raum Meldungen
tab3_layout = [[sg.T('This is inside tab 3')],    
               [sg.In(key='raummeldungen')]] 
#Tab4 - Eingabe
tab4_layout = [[sg.T('Hier können weitere Raumbuchungsanfragen erstellt werden.')],
               #[sg.Radio('Einfachanfragen     ', "anfrage1", default=True, size=(10,1)), sg.Radio('Mehrfachanfragen', "anfrage2")],
                
                #Infos zur Raumanfrage

                [sg.InputCombo([list1[0], list1[1], list1[2], list1[3]], key='raum', size=(20,200)),
                sg.Input('Datum',key='datum', size=(22,200)), sg.InputText(key='start', size=(22,200)),sg.InputText(key='ende', size=(22,200))],
                [sg.InputText(key='person', size=(22,200)), sg.InputText(key = 'produkt', size=(22,200)),
                sg.InputCombo([list2[0], list2[1], list2[2], list2[3], list2[4], list2[5],list2[6]], key='art', size=(20,200)),
                sg.InputCombo([list3[0], list3[1], list3[2]], key='status', size=(20,200))],
                
                [sg.B('Anfrage übernehmen', key= 'ueber')],

                [sg.Output(key = 'Output_Ein')],

                [sg.B('Anfrage(n) speichern', key = 'speichern')]]
            


# Gesamtes Layout und Fenster
layout = [[sg.TabGroup([[sg.Tab('Suche', tab1_layout, tooltip='Toll'), sg.Tab('Wöchentliche Meldungen', 
        tab2_layout), sg.Tab('Raum Meldungen', tab3_layout), sg.Tab('Eingabe', tab4_layout)]], tooltip='Geil')] ]

window = sg.Window('DIE BÜHNE', layout, default_element_size=(100,20)) #create a window


# Event Loop to process "events" and get the "values" of the inputs
while True: 
    event, values = window.read() 
    textInputs_such = values['Input']
    #Values zur Ausgabe
    in_raum = values['raum']
    in_datum = values['datum']
    in_start = values['start']
    in_ende = values['ende']
    in_person = values['person']
    in_produkt = values['produkt']
    in_art = values['art']
    in_status = values['status']

    #Suche
    if event == 'Suchen':  
        window.FindElement('Output').Update('')
        such = textInputs_such
        liste = search_data1(such)
        #for l in liste:
            #print(l)
        window.FindElement('Output').Update(liste)
        #window.FindElement('Output').Update(liste)
        #window.FindElement('Output').Update(search_data1(search))
    if event == 'Infobox':  
        #sg.popup('you entered:', textInputs) #popup is a GUI equivalent of a print statement
        sg.popup("DIE BÜHNE - das Theater der TU Dresden")
    if event == 'Liste Leeren':
        window.FindElement('Output').Update('')
    if event == sg.WIN_CLOSED: 
        break

    #Eingabe
    if event == 'ueber':
        anfrage.append(["2",in_raum,"Freitag", in_datum, in_start, in_ende, in_person, in_produkt, in_art, in_status])
        print(in_raum, in_datum, in_start, in_ende, in_person, in_produkt, in_art, in_status)
    
    if event == 'speichern': 
        save_data(data1 + anfrage)
        sg.popup("Anfragen gespeichert")
        data1 = get_data()
        anfrage = []

window.close()