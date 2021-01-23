
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
    
#Kalender anzeigen lassen
    
import calendar
kalenderblatt = calendar.TextCalendar(calendar.MONDAY)
ausgabe = kalenderblatt.formatmonth(2021,1)
print(ausgabe)

#datei beschreiben
"""
        with open('C:/Users/kairu/OneDrive/7.Semester/Abschlussprojekt/rbl.csv', mode='w') as csv_file:
            #fieldnames = ['ID', 'Raum', 'Wochentag', 'Datum', 'Start', 'Ende', 'Verantwortliche', 'Produktion', 'Nutzungsart','Status']
            writer = csv.writer( delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            #for i in buchung:
            writer.writerows(buchung)
        """
        """
        writer = csv.writer(open('C:/Users/kairu/OneDrive/7.Semester/Abschlussprojekt/rbl.csv', mode='w', delimiter = ";"))
        #writer.writerow(['ID', 'Raum', 'Wochentag', 'Datum', 'Start', 'Ende', 'Verantwortliche', 'Produktion', 'Nutzungsart','Status'])
        writer.writerows(buchung)
        """