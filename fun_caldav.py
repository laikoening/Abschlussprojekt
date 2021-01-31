import csv
#with open('BspListe.csv',encoding="utf8", errors='ignore') as file:
    #reader = csv.reader(file)

    #for row in reader:
        #print(row)        
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
    list=[]
    for value in data:
        print(value[3],value[4],value[5])
        list.append(value[3]),
        list.append(value[4])
        list.append(value[5])
        "A = {0}, B = {1}, C = {2}".format(*list)
        
    i=i+1
    print(list)
get_values()




 
      


        
        