from datetime import datetime 
import caldav 
 
URL = "https://nextcloud05.webo.cloud/remote.php/dav" 
UserName = "anna.gafurova@htw-dresden.de" 
Password = " " 

#Setting up a caldav client object and a principal object
client = caldav.DAVClient(url=URL, username=UserName, password=Password) 
my_principal = client.principal() 

#fetching calendars:
calendars = my_principal.calendars() 

#find a list of calendars in my principal, print their names and url
if calendars: 
    print("your principal has %i calendars:" % len(calendars)) 
    for c in calendars: 
        print(" Name: %s URL: %s" % (c.name, c.url)) 
else: 
    print("your principal has no calendars") 
 
#creating a calendar:
my_new_calendar = my_principal.make_calendar(name="Test calendar") 

#Adding an event to the calendar:
my_event = my_new_calendar.save_event("""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:20210126T060000Z-123401@example.com 
DTSTAMP:20210126T060000Z 
DTSTART:20210126T060000Z 
DTEND:20210127T230000Z 
RRULE:FREQ=YEARLY
LOCATION:My office 
CATEGORIES:Business 
DESCRIPTION:This is a note associated with the meeting
SUMMARY:Meeting
END:VEVENT
END:VCALENDAR
""")