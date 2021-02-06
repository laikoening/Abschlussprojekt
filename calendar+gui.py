import PySimpleGUI as sg 
import csv
from datetime import datetime
from icalendar import Calendar, Event
from pytz import UTC # timezone
import pytz

#Function for getting data from csv file using file directory
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

#Function to put data from csv into lists: list of dtstart, dtend and summary for calendar       
def get_values(csv_data):  
    data = csv_data
    list_with_dtstart_as_str=[] 
    list_with_dtend_as_str=[]
    list_with_summaries=[]

    for value in data:
        list_with_dtstart_as_str.append(value[3]+" "+value[4])
        list_with_dtend_as_str.append(value[3]+" "+value[5])  
        list_with_summaries.append(value[7]+','+value[6]+','+ value[8])   

    return list_with_dtstart_as_str, list_with_dtend_as_str, list_with_summaries


#Convert date string lists into python datetime lists
def strings_to_datetime(list_with_dtstart_as_str,list_with_dtend_as_str):
    
    list_with_dtstart_as_datetime = [datetime.strptime(x,'%d.%m.%Y %H:%M') for x in list_with_dtstart_as_str]
    list_with_dtend_as_datetime = [datetime.strptime(x,'%d.%m.%Y %H:%M') for x in list_with_dtend_as_str]
    return  list_with_dtstart_as_datetime, list_with_dtend_as_datetime

#Function to create calendar  
def create_calendar_with_events(start_time, end_time, SUMMARIS):

    cal = Calendar()
    cal.add('mothod','REQUEST')
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')
    
    #Loop for creationg events parsing data from 
    for y in range(len(start_time)) :    

    #Convert start time to start time with timezone
        without_timezone = start_time[y]
        timezone = pytz.timezone("UTC")
        with_timezone = timezone.localize(without_timezone)
        print(with_timezone)

    #Convert end time to end time with timezone
        without_time = end_time[y]
        timezone = pytz.timezone("UTC")
        with_time = timezone.localize(without_time)

     #Create events
        event = Event()      
        event.add('dtstart', with_timezone)
        event['dtstart'].to_ical()
        event["DTSTART"].params.clear()
        event.add('dtend', with_time)
        event["DTEND"].params.clear()
        event.add('dtstamp', with_timezone)
        event["DTSTAMP"].params.clear()
        event['uid'] = str(y)
        event.add('summary', SUMMARIS[y])
        event.add('priority', 5)
        cal.add_component(event)
    #Save events as ics file    
    f = open('buene_events.ics', 'wb')
    f.write(cal.to_ical())
    f.close()

#sg.theme_previewer() #show all themes
sg.theme('DarkPurple7') #choose a theme    
sg.SetOptions(element_padding=(10, 10))      

# Menu definition     
menu_def = [['Help', 'About...']]  

#Layout creation 
layout = [ [sg.Menu(menu_def, )],
           [sg.Text('Application to parse data from csv to Nextcloud')],
           [sg.T('Enter the path to the SCV file'), sg.InputText(key='Input_SCV_path'), sg.FileBrowse(),
            sg.B('Confirm', key='ConfirmPath')], 
           [sg.B('Create ics file')], 
           [sg.Output(), sg.B('Exit')], 
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
    if event == 'Create ics file':
        start_time_str, end_time_str, SUMMARIS = get_values(scv_date)
        start_time, end_time = strings_to_datetime(start_time_str, end_time_str)
        create_calendar_with_events(start_time, end_time, SUMMARIS)
        print(textInputs)
        
    # Process menu choices  
    if event == 'About...':      
        sg.popup("1)For the application to work, click the 'Browse' Button and find....", "2) Click 'Confirm' button the path is correct")      
  
