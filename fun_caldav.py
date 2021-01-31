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
    for value in data:
        print(value[3],value[4],value[5])
    i=i+1
get_values()




 
      


        
        