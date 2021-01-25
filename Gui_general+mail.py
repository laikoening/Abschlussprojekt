

import PySimpleGUI as sg

import win32com.client as win32


##-----DEFAULT SETTINGS----------------------------------##
bw: dict = {'size':(8,4), 'font':('Ariel', 9), 'button_color':("black","#F8F8F8")}
bt: dict = {'size':(8,4), 'font':('FAriel', 9), 'button_color':("black","#F1EABC")}

##-----WINDOW AND LAYOUT---------------------------------##

layout = [ [sg.Text('Input '),sg.InputText('',size=(35, 10),key='-IN-')],
           [sg.Button('Enter',size=(8,4), font='Ariel 9', button_color=('white','green')),sg.Button('Show mail',**bt),sg.Button('Send mail',**bt), sg.Button('Exit')],
           [sg.Text(key='-OUT-', size=(80, 20))],
          ]

# Create the Window
window = sg.Window('Control panel', layout=layout, background_color="#272533", size=(400, 150))

#test list
x=['some text']

#-----CLICK EVENTS 

def test_click(value):
    liste = []
    try:
        liste.append(value)
    except:
        value is None
    return liste


def send_mail():
   
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)                           # outlook MailItem == 0
    mail.To = 'olena.pokotilova@gmail.com'
    mail.Subject = 'Message subjeact'       
    mail.Body = 'Message body'                             # take text from "Buchungsliste"
    mail.Send()
    
def show_mail():
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)                           # outlook MailItem == 0
    mail.To = 'olena.pokotilova@gmail.com'
    mail.Subject = 'Message subjeact'       
    mail.Body = 'Message body'                             # take text from "Buchungsliste" 
    mail.Display(True)                                     # show and edit mail 

#-----MAIN EVENT LOOP------------------------------------##
while True:
    event, values = window.read()
    print(event)
    if event in (None, 'Exit'):    # if user closes window or clicks quit
        break
    if event == 'Enter':                    
        res=test_click(values['-IN-'])
        window['-OUT-'].update(value=res)
        window['-IN-'].update('')
    if event =='Send mail':
        try:
            send_mail()
        except:
            print ('something went wrong')

    if event == 'Show mail':
        layout2 = [
            [sg.Text((x),size=(35, 10))],                           #sg.Text => x(ext list) == should show the message text
            [sg.Button('Send mail'),sg.Button('Edit mail'), sg.Button('Exit')],
                ]
        window2 = sg.Window('Output').Layout(layout2)
        event, values = window2.Read()
        if event == 'Exit':
            window2.Close()
        if event == 'Edit mail':
            show_mail() 
        if event == 'Send mail':
            try:
                send_mail()
            except:
                print ('something went wrong')

    
        
