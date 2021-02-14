from datetime import datetime 
import caldav 

'''After you have created an ics file and 
uploaded it to the nextcloud, you can manage your events using the CalDav library'''

URL = "https://nextcloud05.webo.cloud/remote.php/dav"
UserName = "anna.gafurova@htw-dresden.de"
Password = "qscwdv@!ABC7"

#Setting up a caldav client object and a principal object
client = caldav.DAVClient(url=URL, username=UserName, password=Password) 
my_principal = client.principal() 

# List up all calendars in Nextcloud through the principal-object
calendars = my_principal.calendars() 
if calendars: 
    print("your principal has %i calendars:" % len(calendars)) 
    for c in calendars: 
        print(" Name: %-20s URL: %s" % (c.name, c.url)) 
else: 
    print("your principal has no calendars") 

#Access calendar events from created ics file 
a_calendar = caldav.Calendar(client=client, url= 'https://nextcloud05.webo.cloud/remote.php/dav/calendars/anna.gafurova@htw-dresden.de/new/') 
events_fetched = a_calendar.date_search(
    start=datetime(2021, 1, 1), end=datetime(2021, 3, 1), expand=True)

#Loop to list up all data from fetched events
for y in range(len(events_fetched)):
    print (y,':', events_fetched[y].data)

#Choose an event from listed events 
event = events_fetched[0]

#Modify event parameters using vobject module and save the event
event.vobject_instance.vevent.summary.value = 'MOMO'
event.vobject_instance.vevent.location.value  = 'BUEHNE'
event.save()
print(event.data)

#Delete (for example) the second event from the calendar
#event1 = events_fetched[2]
#event1.delete()

"""Add an event to your calendar;
!NOTE:each event has own UID. As UID you can write any numbers or words;
There should be no spaces (" ") after each line;
Write DTSTART and DTEND in correct form: "yyyyMMdd'T'HHmmss'Z'" """

evt= """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:lalalala123
DTSTART:20210203T190000Z
DTEND:20210203T223000Z
location:Raum 29
RRULE:FREQ=YEARLY
SUMMARY:Verbrechen 
END:VEVENT
END:VCALENDAR
"""
my_event = a_calendar.save_event(evt)
