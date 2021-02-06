import PySimpleGUI as sg 
import csv
from datetime import datetime
from icalendar import Calendar, Event
from pytz import UTC # timezone
import pytz

def get_data_from_scv(csv_path):
    try:
        with open(rf"{csv_path}", encoding="utf8", errors='ignore') as file:
            reader = csv.reader(file, delimiter=';')
            data_get = []
            for row in reader:
                data_get.append(row)
        return data_get
    except:
        print("Datei nicht gefunden\n")

          
def get_values(csv_data):  
    data = csv_data
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
        event['uid'] = str(y)
        event.add('summary', list3[y])
        event.add('priority', 5)
        cal.add_component(event)
         
    f = open('examp.ics', 'wb')
    f.write(cal.to_ical())
    f.close()

#sg.theme_previewer() #show all themes
sg.theme('DarkPurple7') #choose a theme    
sg.SetOptions(element_padding=(10, 10))      

# menu definition     
menu_def = [['File', ['Open', 'Exit'  ]],           
                ['Help', 'About...'], ]      

#layout creation 
layout = [ [sg.Menu(menu_def, )],
           [sg.Text('Application to parse data from csv to Nextcloud')],
           [sg.T('Enter the path to the SCV file'), sg.InputText(key='Input_SCV_path'), sg.FileBrowse(),
            sg.B('Confirm', key='ConfirmPath')],
           [sg.InputText(key='Input')], 
           [sg.B('To Output'), sg.B('Popup')], 
           [sg.Output(), sg.B('Confirm'), sg.B('Exit')], 
         ]      
window = sg.Window('CSV to Nextcloud parser', layout)

#Loop for buttons choices    
while True:      
    event, values = window.read()   
    scvPath = values['Input_SCV_path'] 
    if event == 'ConfirmPath':
        scv_date = get_data_from_scv(scvPath)
        print(scv_date)
    if event == sg.WIN_CLOSED or event == 'Exit':      
        break            
    textInputs = values['Input'] 
    if event == 'To Output':
        get_values(scv_date)   
        print(textInputs)
    if event == 'Popup':  
        sg.popup('you entered:', textInputs) #popup is a GUI equivalent of a print statement
        
    # Process menu choices  
    if event == 'About...':      
        sg.popup("1)For the application to work, click the 'Browse' Button and find....", "2) Click 'Confirm' button the path is correct")      
    elif event == 'Open':      
        filename = sg.popup_get_file('file to open', no_window=True)      
        print(filename)      