import PySimpleGUI as sg
import pandas as pd
import threading
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

df = pd.read_excel(r'C:\Users\NGUYEN XUAN TRUONG\OneDrive\Tài liệu\Third year\Embedded Systems\test_GUI\RFID.xlsx')
table_data = df.values.tolist()
table_headings = df.columns.values.tolist()

sg.theme("LightBlue")

layout = [
    [sg.Text("Enter Resident Information", size = (40,1), text_color="Black", justification = "Center")],

    [sg.Text('Name', size =(15,1)), sg.Input(key = 'Name', size = (50,4))],
    [sg.Text('Age', size=(15,1)), sg.Input(key = 'Age', size=(10,4)),
    sg.Text('Gender', size=(15,1)), sg.Combo(['Male', 'Female'], key = 'Gender',text_color = 'Black', size = (10,4))],
    [sg.Text('Plate number', size =(15,1)), sg.Input(key = 'Plate number', size = (50,4), do_not_clear = True)],
    [sg.Text('Phone number', size =(15,1)), sg.Input(key = 'Phone number', size = (50,4), do_not_clear = True)],
    [sg.Button('Input ID'), sg.Text('ID: '), sg.Input(key= 'Output_ID')],
    [sg.Button('Save'), sg.Button('Exit')],
    

    [sg.Table(values = table_data,
              headings = ['ID', 'Name', 'Age', 'Gender', 'Plate number', 'Phone number'],
              key = 'Table',
              row_height = 30,
              justification = 'center',
              expand_x = True,
              expand_y = True,
              )]

        ]

window = sg.Window("RFID",layout)

 # NEW WINDOW TO FIND ID
def finding_ID_window():
    reader = SimpleMFRC522()
    ID_reader, text = reader.read()

    finding_ID_layout = [
     [sg.Text('ID Status'), sg.Text(key='ID_Status')],
     [sg.Input(key='ID_code', do_not_clear = True, size=(50,4))],
     [sg.Button('Save')],
     [sg.Button('Exit')]                                             
                        ]

    finding_ID_window = sg.Window('ID Searching ...', finding_ID_layout, modal=True, size= (250,130))

    finding_ID_window['ID_code'].update(ID_reader)
    while True:
        event, values = finding_ID_window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Save':
            validate_id_code(values['ID_code'], finding_ID_window)
            window['Output_ID'].update(values['ID_code'])
            break
        elif event == 'ID_Err':
            finding_ID_window['ID_Status'].update(values[event])    
    finding_ID_window.close()


def validate_id_code(ID_code,window): #FIND ID WITHOUT NEW WINDOW
    if ID_code == '':
        window.write_event_value('ID_Err', 'Please enter a valid ID')
    else:
        try:
            value = int(ID_code)
            id_list = df.values[:,0].tolist()
            if value in id_list:
                window.write_event_value('ID_Err', 'ID already existed')
        except:
            window.write_event_value('ID_Err', 'Please enter a valid ID')  
    

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Input ID':
        finding_ID_window()
    
    elif event == 'Save':
        df = df.append(values, ignore_index = True)
        df.to_excel(r'C:\Users\NGUYEN XUAN TRUONG\OneDrive\Tài liệu\Third year\Embedded Systems\test_GUI\RFID.xlsx', index = False)

window.close()