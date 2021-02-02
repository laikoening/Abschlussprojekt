import csv
from datetime import datetime
import time    
from icalendar import Calendar, Event
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
    #print(date1[1])
    #print(type(date1[1]))
    
    cal = vobject.iCalendar()

    for y in range(len(date1)) :
        
        cal.add('vevent')
        cal.vevent.add('summary').value = list3[y]
        #cal.prettyPrint()
        first_ev = cal.vevent
        utc = vobject.icalendar.utc
        start = cal.vevent.add('dtstart')
        start.value = date1[y]
        end = cal.vevent.add('dtend')
        end.value = date2[y]
        #first_ev.prettyPrint()
        cal.vevent.add('uid').value = 'Sample UID'
        icalstream = cal.serialize()
        #print (icalstream)

    f = open('examp.ics', 'w')
    f.write(icalstream)
    f.close()

get_values()