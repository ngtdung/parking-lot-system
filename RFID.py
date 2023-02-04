import PySimpleGUI as sg
import pandas as pd
from subprocess import call

#from pandas import ExcelFile

df = pd.read_excel(r'C:\Users\NGUYEN XUAN TRUONG\OneDrive\Tài liệu\Third year\Embedded Systems\test_GUI\RFID.xlsx')
table_data = df.values.tolist()
table_headings = df.columns.values.tolist()
#print(table_data)

sg.theme("LightBlue")

layout = [
    [sg.Text("Enter Resident Information", size = (40,1), text_color="Black", justification = "Center")],

    [sg.Text('Name', size =(15,1)), sg.Input(key = 'Name', size = (50,4))],
    [sg.Text('Age', size=(15,1)), sg.Input(key = 'Age', size=(10,4)),
    sg.Text('Gender', size=(15,1)), sg.Combo(['Male', 'Female'], key = 'Gender',text_color = 'Black', size = (10,4))],
    [sg.Text('Plate number', size =(15,1)), sg.Input(key = 'Plate number', size = (50,4))],
    [sg.Text('Phone number', size =(15,1)), sg.Input(key = 'Phone number', size = (50,4))],
    [sg.Button('Find ID', key = 'Find ID')],
    [sg.Button('Save', key = 'Save')],
    

    [sg.Table(values = table_data,
              headings = table_headings,
              key = 'Table',
              row_height = 30,
              justification = 'center',
              expand_x = True,
              expand_y = True,
              )]

        ]

window = sg.Window("RFID",layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Find ID':
        call(["python", "test_waiting.py"])
    if event == 'Save':
        df = df.append(values, ignore_index = True)
        df.to_excel(r'C:\Users\NGUYEN XUAN TRUONG\OneDrive\Tài liệu\Third year\Embedded Systems\test_GUI\RFID.xlsx', index = False)