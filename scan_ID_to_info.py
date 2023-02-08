import PySimpleGUI as sg
import pandas as pd
from mfrc522 import SimpleMFRC522

df = pd.read_excel(r'RFID.xlsx')
table_data = df.values.tolist()
table_headings = df.columns.values.tolist()

sg.theme('LightBlue')

layout = [
    [sg.Button('Check ID of card'), sg.Text('ID: '), sg.Input(key='id_scanned')],
    [sg.Text(key='id_scanned_status')],
    [sg.Button('Exit')],

    [sg.Text(key='info')]
]

window = sg.Window('Scan card', layout, finalize=True)


def show_info(data):
    show_info_layout = [[sg.Text('Name: ' + data[0])],
                        [sg.Text('Age: {}'.format(data[1]))],
                        [sg.Text('Gender: ' + data[2])],
                        [sg.Text('Plate Number: ' + data[3])],
                        [sg.Text('Phone Number: {}'.format(data[4]))],
                        [sg.Text('Card ID: {}'.format(data[5]))],
                        [sg.Button('Exit')]
                        ]
    show_info_window = sg.Window('Resident Info', show_info_layout, size=(290, 290), resizable=True, finalize=True)
    while True:
        evnt, val = show_info_window.read()
        if evnt == sg.WIN_CLOSED or evnt == 'Exit':
            break
    show_info_window.close()


while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == 'Check ID of card':
        reader = SimpleMFRC522()
        ID_reader, text = reader.read()
        window['id_scanned'].update(ID_reader)
        value = int(ID_reader)
        id_list = df.values[:, 5].tolist()
        if value in id_list:
            # show information
            filtered_df = df[df['Output_ID'].notna()].drop(0, axis=1)
            row = filtered_df[filtered_df['Output_ID'] == value].iloc[0]
            info = row.values.tolist()
            show_info(info)
        else:
            window['id_scanned_status'].update('ID is not in list')

window.close()
