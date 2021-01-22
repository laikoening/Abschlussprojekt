
#Einlesen der Daten

#witzige, aber sinnlos anmutende Idee
         id, raum, tag, datum, start, ende, person, produk, art, status = [], [], [], [], [], [], [], [], [], []

        for row in reader:
            print (row)
            id.append(int(row[0]))
            raum.append(row[1])
            tag.append(row[2])
            datum.append(row[3])
            start.append(row[4])
            ende.append(row[5])
            person.append(row[6])
            produk.append(row[7])
            art.append(row[8])
            status.append(row[9])
        #mehrdimensionales array
        buchungen = np.array([id, raum, tag, datum, start, ende, person, produk, art, status]) 
        #Zugriff auf mehrdimensionales Array
        #print (buchungen[0:9,0])
    
