import csv
from datetime import datetime
import time
     
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
    for value in data:
        list1.append(value[3]+" "+value[4])
        list2.append(value[3]+" "+value[5])

            
    i=i+1
    print(list1)
    print("----------------")
    print(list2)
    
    #date string list to python datetime list
    
    date1 = [datetime.strptime(x,'%d.%m.%Y %H:%M') for x in list1]
    print(date1)

    date2 = [datetime.strptime(x,'%d.%m.%Y %H:%M') for x in list2]
    print(date2)


get_values()




 
      


        
        