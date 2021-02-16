import PySimpleGUI as sg 
import csv
from datetime import datetime
from icalendar import Calendar, Event
from pytz import UTC # timezone
import pytz

def get_data_from_csv(csv_path):
    '''
       Function for getting data from csv file using file directory
       Args: chosen csv-file path 
       Raises: error message in case of incorrect format of the chosen file 
       Returns: list
    '''
    try:
        with open(rf"{csv_path}", encoding="utf8", errors='ignore') as file:
            reader = csv.reader(file, delimiter=';')
            data_get = []
            for row in reader:
                data_get.append(row)
        return data_get
    except:
        print("File can't be read, please check the file format\n")

def get_values(csv_data):
    '''
       Function to extract data for calendar.
       Arg: list with data (booking data for rehearsals and performances) from csv file
       Returns: string list with start dates of events, string list with end dates of events, 
       string list with summaries, string list with locations
    ''' 
    data = csv_data
    list_with_dtstart_as_str=[] 
    list_with_dtend_as_str=[]
    list_with_summaries=[]
    list_with_location=[]
    for value in data:
        list_with_dtstart_as_str.append(value[3]+" "+value[4])         # date string + start time string
        list_with_dtend_as_str.append(value[3]+" "+value[5])           # date string + end time string
        list_with_summaries.append(value[7]+','+value[6]+','+ value[8]) # list with names of plays, responsible people, status(rehearsals or performances) as summary list for calendar
        list_with_location.append(value[1]) 

    return list_with_dtstart_as_str, list_with_dtend_as_str, list_with_summaries,list_with_location

def strings_to_datetime(list_with_dtstart_as_str,list_with_dtend_as_str):
    '''
       Function to convert string list with start dates and string list with end dates 
       into python datetime lists
    '''  
    list_with_dtstart_as_datetime = [datetime.strptime(x,'%d.%m.%Y %H:%M') for x in list_with_dtstart_as_str]
    list_with_dtend_as_datetime = [datetime.strptime(x,'%d.%m.%Y %H:%M') for x in list_with_dtend_as_str]
    return  list_with_dtstart_as_datetime, list_with_dtend_as_datetime

def create_calendar_with_events(start_time, end_time, SUMMARIS,LOCATION):
    '''
       Function to create calendar with events and save them as isc file
       Arg: datetime list of start dates, datetime list of end dates, 
       string list of summaries, string list of locations
    '''
    cal = Calendar()   # init the calendar

# Some properties are required to be compliant:
    cal.add('mothod','REQUEST')
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

# Loop for creation events using lists with start dates, end dates, summaries and locations:
    for y in range(len(start_time)) :    

    # Convert each start time to start time with timezone
        without_timezone = start_time[y]
        timezone = pytz.timezone("UTC")
        start_time_with_tz = timezone.localize(without_timezone)

    # Convert end time to end time with timezone
        without_tz = end_time[y]
        timezone = pytz.timezone("UTC")
        end_time_with_tz = timezone.localize(without_tz)

     # Create events
        event = Event()      
        event.add('dtstart', start_time_with_tz)
        event["DTSTART"].params.clear()          
        event.add('dtend', end_time_with_tz)  # add start date of an event to calendar event 
        event["DTEND"].params.clear()
        event.add('dtstamp', start_time_with_tz)
        event["DTSTAMP"].params.clear()
        event['uid'] = str(y)                
        event.add('summary', SUMMARIS[y])   # add event sumarry to calendar event
        event.add('location', LOCATION[y])  # add event location to calendar event
        event.add('priority', 5)
        cal.add_component(event)  # add events to the calendar

    # Save events as ics file    
    f = open('buene_events.ics', 'wb')
    f.write(cal.to_ical())
    f.close()

# Interface creation
sg.theme_previewer() #show all themes
sg.theme('DarkPurple7') #choose a theme    
sg.SetOptions(element_padding=(10, 10))      

# Menu definition     
menu_def = [['HELP', 'How to use the application']]  

# Layout creation 
layout = [ [sg.Menu(menu_def, )],
           [sg.Text('Application to parse data from csv to Nextcloud')],
           [sg.T('Enter the path to the csv file'), sg.InputText(key='Input_CSV_path'), sg.FileBrowse(),
            sg.B('Confirm', key='ConfirmPath')], 
           [sg.B('Create ics file')], 
           [sg.Output(), sg.B('Exit')]
         ]      
window = sg.Window('CSV to Nextcloud parser', layout)

# Loop to choose buttons  
while True:      
    event, values = window.read()   
    scvPath = values['Input_CSV_path'] 

    if event == 'ConfirmPath':
        csv_date = get_data_from_csv(scvPath)
        print(csv_date)    # show read data from csv

    if event == sg.WIN_CLOSED or event == 'Exit':      
        break            
     
    if event == 'Create ics file':
        start_time_str, end_time_str, SUMMARIS,LOCATION = get_values(csv_date)
        start_time, end_time = strings_to_datetime(start_time_str, end_time_str)
        create_calendar_with_events(start_time, end_time, SUMMARIS,LOCATION)
  
    # Process menu choices  
    if event == 'How to use the application':      
        sg.popup("Step 1: For the application to work, click 'Browse' and select the requireed file",  # popup is a GUI equivalent of a print statement
                 "Step 2: Click 'Confirm' if the path is correct",
                 "Step 3: Click  'Create isc file'",
                 "Step 4: Upload the created ics file to your Nextcloud calendar")      
  
window.close()

