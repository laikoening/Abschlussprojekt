import csv
from datetime import datetime
import time
    
from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC # timezone
import vobject
import pytz

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
    i=0
    list1=[] 
    list2=[]
    list3=[]
    for value in data:
        list1.append(value[3]+" "+value[4])
        list2.append(value[3]+" "+value[5])  
        list3.append(value[7]+','+value[6]+','+ value[8])         
    i=i+1
    print(list1)
    #print("----------------")
    #print(list2)
    #print(list3)
    print(type(list3[1]))
    #date string list to python datetime list
    date1 = [datetime.strptime(x,'%d.%m.%Y %H:%M') for x in list1]
    print(date1)
    print("-----------")
    #print(date1[1])
    date2 = [datetime.strptime(x,'%d.%m.%Y %H:%M') for x in list2]
    #print(date2)
    print(date1[1])
    print(type(date1[1]))
    #iso format 
    #some_date = date1[1]
    #iso_date_string = some_date.isoformat()
    #print(iso_date_string)

    #add timezone to datetime

    #without_timezone = date1[1]
    #timezone = pytz.timezone("UTC")
    #with_timezone = timezone.localize(without_timezone)
    #print(with_timezone)

    #put data from the list into calendar dtstart
    
    cal = Calendar()
    cal.add('mothod','REQUEST')
    #cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')
    

    for y in range(len(date1)) :    
        #print(y,type(y))
        without_timezone = date1[y]
        timezone = pytz.timezone("UTC")
        with_timezone = timezone.localize(without_timezone)
        #print(with_timezone)
        #print(type(with_timezone))
        without_time = date2[y]
        timezone = pytz.timezone("UTC")
        with_time = timezone.localize(without_time)
        

        event = Event()      
        event.add('summary', list3[y])
        event.add('dtstart', with_timezone)
        #event.add("dtstart",pytz.utc.localize(date1[y]))
        event.add('dtend', with_time)
        event.add('dtstamp', with_timezone)
        event['uid'] = '20050115T101010/27346262376@mxm.dk'
        event.add('priority', 5)
        cal.add_component(event)
        

    
    f = open('examp.ics', 'wb')
    f.write(cal.to_ical())
    f.close()

get_values()


 
      


        
        