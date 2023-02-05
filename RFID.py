import PySimpleGUI as sg
import pandas as pd
import threading
#from mfrc522 import SimpleMFRC522

#reader = SimpleMFRC522()


df = pd.read_excel(r'C:\Users\NGUYEN XUAN TRUONG\OneDrive\Tài liệu\Third year\Embedded Systems\test_GUI\RFID.xlsx')
table_data = df.values.tolist()
table_headings = df.columns.values.tolist()
print(table_data)

sg.theme("LightBlue")

layout = [
    [sg.Text("Enter Resident Information", size = (40,1), text_color="Black", justification = "Center")],

    [sg.Text('Name', size =(15,1)), sg.Input(key = 'Name', size = (50,4))],
    [sg.Text('Age', size=(15,1)), sg.Input(key = 'Age', size=(10,4)),
    sg.Text('Gender', size=(15,1)), sg.Combo(['Male', 'Female'], key = 'Gender',text_color = 'Black', size = (10,4))],
    [sg.Text('Plate number', size =(15,1)), sg.Input(key = 'Plate number', size = (50,4), do_not_clear = True)],
    [sg.Text('Phone number', size =(15,1)), sg.Input(key = 'Phone number', size = (50,4), do_not_clear = True)],
    [sg.Button('Find ID'), sg.Text('ID: '), sg.Text(key='Output_ID'),],
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

""" # NEW WINDOW TO FIND ID
def finding_ID_window():
    finding_ID_layout = [
     [sg.Text("Searching ...", size=(20,1), justification = "Center")],
     [sg.Input(key='ID', do_not_clear = True, size=(50,4))],
     [sg.Button('Save')],
     [sg.Button('Exit')]                                             
                        ]

    finding_ID_window = sg.Window('ID Searching ...', finding_ID_layout, modal=True, size= (250,130))

    while True:
        event, values = finding_ID_window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Save':
            try:
                values['ID'] = int(values['ID'])
            except ValueError:
                window.write_event_value('Please enter a valid ID', None)
                continue
            else:
                window.write_event_value('ID: ', values['ID'])
                window['ID'].update(values['Output_ID'])
                break
        
    
    finding_ID_window.close()
"""

def search(ID_code): #FIND ID WITHOUT NEW WINDOW
    while ID_code == None:
        try:
            values['ID'] = int(values['ID'])
        except ValueError:
            continue
        else:
            break
window.write_event_value('Done', None)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Find ID':
        reader = SimpleMFRC522()
        ID_code, text = reader.read()
        window['Output_ID'].update('Searching ...')
        threading.Thread(target= search, args=(ID_code)).start()
    elif event == 'Done':
        window['Done'].update(ID_code)
    elif event == 'Save':
        df = df.append(values, ignore_index = True)
        df.to_excel(r'C:\Users\NGUYEN XUAN TRUONG\OneDrive\Tài liệu\Third year\Embedded Systems\test_GUI\RFID.xlsx', index = False)
window.close()