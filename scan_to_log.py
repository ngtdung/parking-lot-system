import PySimpleGUI as sg
import pandas as pd
from mfrc522 import SimpleMFRC522
import plate_detection as pld
from scan_ID_to_info import show_info
import logr as lr
import test_cam as tc
import time
import cv2
from openpyxl import Workbook, load_workbook
from picamera2 import Picamera2, Preview
from PIL import Image

df = pd.read_excel(r'RFID.xlsx')
sg.theme('LightBlue')

layout = [
    [sg.Button('Scan ID'), sg.Input(key='ID_scanned', do_not_clear=True, size=(50, 4)), sg.Text(key='ID_status')],
    [sg.Button('Exit')],
]

window = sg.Window('Create daily ticket', layout)
            

def extract_plate_from_log(ID, wb, row_value):
    ws = wb['Sheet1']
    if row_value > 0:
        print('out')
        entry_plate = ws.cell(row=row_value, column=4).value
        exit_plate = ws.cell(row=row_value, column=5).value
        Image.open(entry_plate).show()
        Image.open(exit_plate).show()
    else:
        print('in')
        entry_plate = ws.cell(row=ws.max_row, column=4).value
        Image.open(entry_plate).show()
    

def validate_id_code(ID_code):
    if ID_code == '':
        return 'Please enter a valid ID'
    else:
        value = int(ID_code)
        id_list = df.values[:, 5].tolist()
        if value in id_list:
            # show information
            return 'Monthly ticket'
        else:
            return 'Daily ticket'


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Scan ID':
        wb = load_workbook(filename="Log.xlsx")
        reader = SimpleMFRC522()
        ID_reader,text = reader.read()
        row_val = lr.check(ID_reader, wb)
        window['ID_scanned'].update(ID_reader)
        error_message = validate_id_code(ID_reader)
        if error_message == 'Please enter a valid ID':
            window['ID_status'].update(error_message)
        elif error_message == 'Monthly ticket':
            window['ID_status'].update(error_message)
            filtered_df = df[df['Output_ID'].notna()].drop(0, axis=1)
            row = filtered_df[filtered_df['Output_ID'] == int(ID_reader)].iloc[0]
            info = row.values.tolist()
            show_info(info)
        elif error_message == 'Daily ticket':
            window['ID_status'].update(error_message)
        #img_path = tc.take_picture(ID_reader)
        img_path = 'entry_test.jpg'
        pld.plate_retrieval(img_path, row_val)
        lr.log(wb, ID_reader, img_path, row_val)
        extract_plate_from_log(ID_reader, wb, row_val)
window.close()
