import PySimpleGUI as sg
import pandas as pd
from mfrc522 import SimpleMFRC522
import log as lg

reader = SimpleMFRC522()

df = pd.read_excel(r'RFID.xlsx')

sg.theme('LightBlue')

layout = [
    [sg.Button('Scan ID'), sg.Input(key='ID_scanned', do_not_clear = True, size=(50,4)), sg.Text(key = 'ID_status')],
    [sg.Button('Exit')]
]

window = sg.Window('Create daily ticket', layout)

def validate_id_code(ID_code):
    if ID_code == '':
        return 'Please enter a valid ID'
    else:
        value = int(ID_code)
        id_list = df.values[:,5].tolist()
        if value in id_list:
            return 'ID already existed'

while True:
    event, values = window.read()
    if event == sg.WIN.CLOSED or event == 'Exit':
        break
    elif event == 'Scan ID':
        reader = SimpleMFRC522()
        ID_reader, text = reader.read()
        window['ID_scanned'].update(ID_reader)
        error_message = validate_id_code(values['ID_code'])
        if error_message:
            window['ID_status'].update(error_message)
        else: 
            window['ID_scanned'].update(values['ID_code'])
            window['ID_status'].update('Saved')
            df = df.append(values, ignore_index = True)
            df.to_excel(r'Log.xlsx', index = False)
            lg.login(ID_reader)
window.close()


