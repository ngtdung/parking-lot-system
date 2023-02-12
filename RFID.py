# Import libraries
import PySimpleGUI as sg
import pandas as pd
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()  # Initialize RFID Reader Object

df = pd.read_excel(r'RFID.xlsx')  # Import data from monthly ticket into dataframe
table_data = df.values.tolist()  # Get table's data
table_headings = df.columns.values.tolist()  # Get table's headings

sg.theme("LightBlue")  # Set theme

# Set layout for the GUI
layout = [
    [sg.Text("Enter Resident Information", size=(40, 1), text_color="Black", justification="Center")],

    [sg.Text('Name', size=(15, 1)), sg.Input(key='Name', size=(50, 4))],
    [sg.Text('Age', size=(15, 1)), sg.Input(key='Age', size=(10, 4)),
     sg.Text('Gender', size=(15, 1)), sg.Combo(['Male', 'Female'], key='Gender', text_color='Black', size=(10, 4))],
    [sg.Text('Plate number', size=(15, 1)), sg.Input(key='Plate number', size=(50, 4), do_not_clear=True)],
    [sg.Text('Phone number', size=(15, 1)), sg.Input(key='Phone number', size=(50, 4), do_not_clear=True)],
    [sg.Button('Input ID'), sg.Text('ID: '), sg.Input(key='Output_ID')],
    [sg.Button('Save'), sg.Button('Exit'), sg.Text(key='input_err')],

    [sg.Table(values=table_data,
              headings=table_headings,
              row_height=30,
              justification='center',
              expand_x=True,
              expand_y=True,
              )]

]

window = sg.Window("RFID", layout)  # Initialize the Window


# NEW WINDOW TO FIND ID
def finding_ID_window():
    reader = SimpleMFRC522()
    ID_reader, text = reader.read()
    finding_ID_layout = [
        [sg.Text('ID Status'), sg.Text(key='ID_Status')],
        [sg.Input(key='ID_code', do_not_clear=True, size=(50, 4))],
        [sg.Button('Save')],
        [sg.Button('Exit')]
    ]
    finding_ID_window = sg.Window('ID Searching ...', finding_ID_layout, modal=True, size=(250, 130), finalize=True)

    finding_ID_window['ID_code'].update(ID_reader)
    while True:
        event, values = finding_ID_window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Save':
            error_message = validate_id_code(values['ID_code'], finding_ID_window)
            if error_message:
                finding_ID_window['ID_Status'].update(error_message)
            else:
                window['Output_ID'].update(values['ID_code'])
                break

    finding_ID_window.close()


def validate_id_code(ID_code, window):  # FIND ID WITHOUT NEW WINDOW
    if ID_code == '':
        return 'Please enter a valid ID'
    else:
        value = int(ID_code)
        id_list = df.values[:, 5].tolist()
        if value in id_list:
            return 'ID already existed'


# Function to check the form is completely filled
def check_input(values_input):
    try:
        inputs_to_check = ['Name', 'Age', 'Gender', 'Plate number', 'Phone number', 'Output_ID']
        for x in inputs_to_check:
            if values_input[x] == '':
                return False
        return True
    except KeyError:
        return False


# Function to clear form after saving
def wipe(values):
    inputs_to_wipe = ['Name', 'Age', 'Gender', 'Plate number', 'Phone number', 'Output_ID']
    for i in inputs_to_wipe:
        window[inputs_to_wipe].update('')


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Input ID':
        finding_ID_window()

    elif event == 'Save':
        input_err = check_input(values)
        if input_err:
            id_list = df.values[:, 5].tolist()
            if int(values['Output_ID']) in id_list:
                window['input_err'].update('ID already exists, please input a new ID')
            else:
                df = df.append(values, ignore_index=True)
                df.to_excel(r'RFID.xlsx', index=False)
                window['Name'].update('')
                window['Age'].update('')
                window['Gender'].update('')
                window['Phone number'].update('')
                window['Plate number'].update('')
                window['Output_ID'].update('')

        else:
            window['input_err'].update('Input Error: One or more information are missing')

window.close()
