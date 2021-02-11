from datetime import datetime 
import caldav 
import vobject
import csv

 
URL = "https://nextcloud05.webo.cloud/remote.php/dav" 
UserName = "anna.gafurova@htw-dresden.de" 
Password = "Tr" 

client = caldav.DAVClient(url=URL, username=UserName, password=Password) 
my_principal = client.principal() 
calendars = my_principal.calendars() 
my_new_calendar = 0

def get_data():
    try:
        with open('BspListe.csv', encoding="utf8", errors='ignore') as file:
            reader = csv.reader(file, delimiter=';')
            data_get = []
            for row in reader:
                data_get.append(row)
        return data_get
    except:
        print("Datei nicht gefunden\n")

def get_values():  
    data = get_data() 
    try:
        my_new_calendar = my_principal.make_calendar(name="Name") 
        
    except: 
        print("can not make a calendar")
    
    for y in range(len(data)):
        location = data[y]
        dtstart,dtend = date_to_right_date(data[y][3],data[y][4], data[y][5])
        summary = data[y][7] + ',' + data[y][6], +','+data[y][8]
        event = create_event(str(i + 1), dtstart, dtend, location, summary)
        parse_ebent(my_new_calendar, event)

def date_to_right_date
def crete_event ()
vcal = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:20210126T060000Z-123401@example.com
DTSTAMP:20210126T060000Z
DTSTART:%s
DTEND:%s
RRULE:FREQ=YEARLY
LOCATION:%s
CATEGORIES:Business
DESCRIPTION:This is a note associated with the meeting
SUMMARY:meeting
END:VEVENT
END:VCALENDAR
""" % (DTSTART, DTEND, location)


    
events_fetched = my_new_calendar.date_search(
    start=datetime(2020, 1, 1), end=datetime(2022, 1, 1), expand=True)
print(events_fetched[0].data)

event = events_fetched[0]

event.vobject_instance.vevent.summary.value = 'hello'
event.save()



#my_principal.calendars() 
 
#if calendars: 
    #print("your principal has %i calendars:" % len(calendars)) 
    #for c in calendars: 
        #print(" Name: %-20s URL: %s" % (c.name, c.url)) 
    #else: 
        #print("your principal has no calendars") 