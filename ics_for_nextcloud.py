import csv
from datetime import datetime   
from icalendar import Calendar, Event
from pytz import UTC # timezone
import vobject

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
    #print(data)
    i=0
    list1=[] 
    list2=[]
    list3=[]
    for value in data:
        list1.append(value[3]+" "+value[4])
        list2.append(value[3]+" "+value[5])  
        list3.append(value[7]+','+value[6]+','+ value[8])         
    i=i+1
   
    print(type(list3[1]))

    #date string list to python datetime list
    date1 = [datetime.strptime(x,'%d.%m.%Y %H:%M') for x in list1]
    #print(date1)
    print("-----------")
    #print(date1[1])
    date2 = [datetime.strptime(x,'%d.%m.%Y %H:%M') for x in list2]
    
    list4=[]
    list4.append(date1)
    list4.append(date2)
    list4.append(list3)
    print(list4)

    #print(date2)
    #print(date1[1])
    #print(type(date1[1]))
    
    f = open('examp.ics', 'w')
    
    for y in range(len(list4[0])):
        cal = vobject.iCalendar()
        cal.add('vevent')
        cal.vevent.add('summary').value = list4[2][y]
        utc = vobject.icalendar.utc
        start = cal.vevent.add('dtstart')
        start.value = list4[0][y]
        end = cal.vevent.add('dtend')
        end.value = list4[1][y]
        cal.vevent.add('uid').value = 'Sample UID'
        
        icalstream = cal.serialize()
        print (icalstream) 
        
        f.write(icalstream)
    f.close()
   
get_values()
