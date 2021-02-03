import PySimpleGUI as sg 
import csv
from datetime import datetime
from icalendar import Calendar, Event
from pytz import UTC # timezone
import pytz
import vobject

def get_data():
    while True:
        try:
            with open('BspListe.csv',encoding="utf8", errors='ignore') as file:
                reader = csv.reader(file,delimiter=';')
                data_get = []
                for row in reader:
                    data_get.append(row)
            return data_get
        except:
            print("Datei nicht gefunden\n")
          
def get_values():  
    data=get_data()
    list1=[] 
    list2=[]
    list3=[]
    for value in data:
        list1.append(value[3]+" "+value[4])
        list2.append(value[3]+" "+value[5])  
        list3.append(value[7]+','+value[6]+','+ value[8])         
    
    #date string list to python datetime list
    date1 = [datetime.strptime(x,'%d.%m.%Y %H:%M') for x in list1]
    print(date1)
    print("-----------")
    date2 = [datetime.strptime(x,'%d.%m.%Y %H:%M') for x in list2]
   
    #put data from the list into calendar dtstart   
    cal = Calendar()
    cal.add('mothod','REQUEST')
    #cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')
   
    for y in range(len(date1)) :    
        
        without_timezone = date1[y]
        timezone = pytz.timezone("UTC")
        with_timezone = timezone.localize(without_timezone)
        print(with_timezone)
        print(type(with_timezone))
        without_time = date2[y]
        timezone = pytz.timezone("UTC")
        with_time = timezone.localize(without_time)
        
        event = Event()      
    
        event.add('dtstart', with_timezone)
        event['dtstart'].to_ical()
        event["DTSTART"].params.clear()
        event.add('dtend', with_time)
        event["DTEND"].params.clear()
        event.add('dtstamp', with_timezone)
        event["DTSTAMP"].params.clear()
        #event['uid'] = '20050115T101010/27346262376@mxm.dk'
        event.add('summary', list3[y])
        #event.add('priority', 5)
        cal.add_component(event)
         
    f = open('examp.ics', 'wb')
    f.write(cal.to_ical())
    f.close()

#sg.theme_previewer() #show all themes
sg.theme('DarkPurple7') #choose a theme    
sg.SetOptions(element_padding=(10, 10))      

    # ------ Menu Definition ------ #      
menu_def = [['File', ['Open', 'Exit'  ]],           
                ['Help', 'About...'], ]      

    # ------ GUI Defintion ------ #      
layout = [ [sg.Menu(menu_def, )],
           [sg.Text('Application to parse data from csv to Nextcloud')],
           [sg.InputText(key='Input')], 
           [sg.B('To Output'), sg.B('Popup')], 
           [sg.Output(), sg.B('Confirm'), sg.B('Exit')], 
         ]      
window = sg.Window('CSV to Nextcloud parser', layout)
 
    # ------ Loop & Process button menu choices ------ #      
while True:      
    event, values = window.read()      
    if event == sg.WIN_CLOSED or event == 'Exit':      
        break            
    textInputs = values['Input'] 
    if event == 'To Output':
        get_values()   
        print(textInputs)
    if event == 'Popup':  
        sg.popup('you entered:', textInputs) #popup is a GUI equivalent of a print statement
        
    # ------ Process menu choices ------ #      
    if event == 'About...':      
        sg.popup("1)For the application to work, click the 'Browse' Button and find....", "2) Click 'Confirm' button the path is correct")      
    elif event == 'Open':      
        filename = sg.popup_get_file('file to open', no_window=True)      
        print(filename)      