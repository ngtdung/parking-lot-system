# Import libraries
import PySimpleGUI as sg
import pandas as pd
from mfrc522 import SimpleMFRC522

df = pd.read_excel(r'RFID.xlsx')

sg.theme('Light Blue')

layout = [
    [sg.Button('Scan ID of card'), sg.Text('ID: '),
     sg.Input(key='id_scanned')],
    [sg.Text(key='id_scanned_status')],
    [sg.Button('Exit')],
    [sg.Text(key='info')]
]

window = sg.Window('Scan card', layout, finalize=True)

# Function to display card's info
def show_info(data, id):
    show_info_layout = [[sg.Text('Name: ' + data.loc[df['Output_ID'] == id, 'Name'].iloc[0])],
                        [sg.Text('Age: {}'.format(data.loc[df['Output_ID'] == id, 'Age'].iloc[0]))],
                        [sg.Text('Gender: ' + data.loc[df['Output_ID'] == id, 'Gender'].iloc[0])],
                        [sg.Text('Plate Number: {}'.format(data.loc[df['Output_ID'] == id, 'Plate number'].iloc[0]))],
                        [sg.Text('Phone Number: {}'.format(data.loc[df['Output_ID'] == id, 'Phone number'].iloc[0]))],
                        [sg.Text('Card ID: {}'.format(id))],
                        [sg.Button('Delete Profile'),
                         sg.Button('Exit')]]

    show_info_window = sg.Window('Resident Info', show_info_layout, size=(290, 290), resizable=True, finalize=True)
    while True:
        evnt, val = show_info_window.read()
        if evnt == sg.WIN_CLOSED or evnt == 'Exit':
            break
        elif evnt == 'Delete Profile':
            warning_prompt(data, id)
            break

    show_info_window.close()

# Function to delete profile from system
def warning_prompt(dataframe, id):
    warning_layout = [[sg.Text('Are you sure?')],
                      [sg.Button('Yes'), sg.Button('No')]]
    warning_window = sg.Window('Warning', warning_layout, finalize=True)
    while True:
        warn_event, warn_val = warning_window.read()
        if warn_event == sg.WIN_CLOSED or warn_event == 'No':
            break
        elif warn_event == 'Yes':
            dataframe.drop(dataframe[dataframe['Output_ID'] == id].index, inplace=True)
            dataframe.to_excel(r'RFID.xlsx', index=False)
            dataframe.reset_index()
            break
    warning_window.close()


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Scan ID of card':
        reader = SimpleMFRC522()
        ID_reader, text = reader.read()
        window['id_scanned'].update(ID_reader)
        value = int(ID_reader)
        id_list = df.values[:, 5].tolist()
        if value in id_list:
            # show information
            filtered_df = df[df['Output_ID'].notna()]
            row = filtered_df[filtered_df['Output_ID'] == value].iloc[0]
            info = row.values.tolist()
            show_info(df, ID_reader)
        else:
            window['id_scanned_status'].update('ID is not in list')

window.close()

