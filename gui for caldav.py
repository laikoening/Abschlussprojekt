import PySimpleGUI as sg 
from datetime import datetime 
import caldav 

def bumbum():
    DTSTART = "20210129T060000Z" 
    DTEND = "20210129T230000Z" 
    location = "MY OFFICE" 
 
    URL = "https://nextcloud05.webo.cloud/remote.php/dav" 
    UserName = "anna.gafurova@htw-dresden.de" 
    Password = "Tratatagidro2017ABC@" 
 
    client = caldav.DAVClient(url=URL, username=UserName, password=Password) 
    my_principal = client.principal() 
    #my_principal.calendars() 
 
    #if calendars: 
        #print("your principal has %i calendars:" % len(calendars)) 
        #for c in calendars: 
            #print(" Name: %-20s URL: %s" % (c.name, c.url)) 
    #else: 
        #print("your principal has no calendars") 
    
    my_new_calendar = my_principal.make_calendar(name="SASeu")  
 
    #print(my_new_calendar) 

    my_new_calendar.save_event("""BEGIN:VCALENDAR
    VERSION:2.0
    PRODID:-//Example Corp.//CalDAV Client//EN
    BEGIN:VEVENT
    UID:20200516T060000Z-123401@example.com
    DTSTAMP:20210516T060000Z
    DTSTART:"""+DTSTART+"""
    DTEND:"""+DTEND+"""
    location:"""+location+"""
    RRULE:FREQ=YEARLY
    SUMMARY:Do the needful
    END:VEVENT
    END:VCALENDAR
    """)
     
sg.theme_previewer() #show all themes
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
        bumbum()   
        print(textInputs)
    if event == 'Popup':  
        sg.popup('you entered:', textInputs) #popup is a GUI equivalent of a print statement
        
    # ------ Process menu choices ------ #      
    if event == 'About...':      
        sg.popup("1)For the application to work, click the 'Browse' Button and find....", "2) Click 'Confirm' button the path is correct")      
    elif event == 'Open':      
        filename = sg.popup_get_file('file to open', no_window=True)      
        print(filename)      