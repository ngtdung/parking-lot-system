import PySimpleGUI as sg
import pandas as pd
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

df = pd.read_excel(r'RFID.xlsx')
table_data = df.values.tolist()
table_headings = df.columns.values.tolist()

sg.theme('LightBlue')

layout = [
    [sg.Button('Check ID of card'),sg.Text('ID: '), sg.Input(key= 'id_scanned')],
    [sg.Text(key= 'id_scanned_status')],
    [sg.Button('Exit')],
    
    [sg.Text(key='info')]
]

window = sg.Window('Scan card', layout, finalize = True)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == 'Check ID of card':
        reader = SimpleMFRC522()
        ID_reader, text = reader.read()
        window['id_scanned'].update(ID_reader)
        value = int(ID_reader)
        id_list = df.values[:,5].tolist()
        if value in id_list:
            #show information
            info = df[df['F'] == value]
            window['info'].update(info)
        else:
            window['id_scanned_status'].update('ID is not in list')

window.close()