import PySimpleGUI as sg 

sg.theme_previewer() #show all themes
sg.theme('DarkPurple7') #choose a theme

layout = [[sg.Text('Raumverwaltung DIE BÜHNE e.V')], 
 [sg.InputText(key='Input')], 
 [sg.B('To Output'), sg.B('Smth'), sg.B('Popup')], 
 [sg.Output(), sg.B('Exit')]] 

window = sg.Window('DIE BÜHNE', layout) #create a window

# Event Loop to process "events" and get the "values" of the inputs
while True: 
 event, values = window.read() 
 textInputs = values['Input'] 
 if event == 'To Output':  
     print(textInputs) 
 if event == 'Popup':  
     sg.popup('you entered:', textInputs) #popup is a GUI equivalent of a print statement
 if event == sg.WIN_CLOSED or event == 'Exit': 
     break 
window.close()