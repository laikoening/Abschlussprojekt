from datetime import datetime 
import caldav 
 
 
DTSTART = "20210126T060000Z" 
DTEND = "20210127T230000Z" 
 
location = "MY OFFICE" 
 
URL = "https://nextcloud05.webo.cloud/remote.php/dav" 
UserName = "anna.gafurova@htw-dresden.de" 
Password = "" 
 
client = caldav.DAVClient(url=URL, username=UserName, password=Password) 
my_principal = client.principal() 
calendars = my_principal.calendars() 
 
if calendars: 
    print("your principal has %i calendars:" % len(calendars)) 
    for c in calendars: 
        print(" Name: %-20s URL: %s" % (c.name, c.url)) 
else: 
    print("your principal has no calendars") 
 
my_new_calendar = my_principal.make_calendar(name="SASeu") 
 
print(my_new_calendar) 
 
my_event = my_new_calendar.save_event("""BEGIN:VCALENDAR
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
SUMMARY:Do the needful
END:VEVENT
END:VCALENDAR
""" % (DTSTART, DTEND, location))

 
print('Hello %s, %s' % (DTSTART, DTEND))
