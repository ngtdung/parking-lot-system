import PySimpleGUI as sg
import pandas as pd
from mfrc522 import SimpleMFRC522
import plate_detection as pld
import logr as lr
import scan_ID_to_info as Sci
import time
from openpyxl import Workbook, load_workbook
import xlsxwriter as xlw
from picamera2 import Picamera2, Preview

# reader = SimpleMFRC522()
df = pd.read_excel(r'RFID.py')
wb = load_workbook(filename="Log.xlsx")
ws = wb['Sheet1']
sg.theme('LightBlue')

layout = [
    [sg.Button('Scan ID'), sg.Input(key='ID_scanned', do_not_clear=True, size=(50, 4)), sg.Text(key='ID_status')],
    [sg.Button('Exit')]
]

window = sg.Window('Create daily ticket', layout)


def take_picture(id):
    picam = Picamera2()

    config = picam.create_preview_configuration()
    picam.configure(config)

    picam.start_preview(Preview.QTGL)

    picam.start()
    time.sleep(2)
    path = str(id) + time.localtime().strftime('%H%M%S')
    path_complete = "{}.jpg".format(path)
    picam.capture_file(path_complete)
    picam.close()
    return path_complete


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
        # reader = SimpleMFRC522()
        ID_reader = 123456789
        window['ID_scanned'].update(ID_reader)
        error_message = validate_id_code(values['ID_code'])
        if error_message == 'Please enter a valid ID':
            window['ID_status'].update(error_message)
        elif error_message == 'Monthly ticket':
            window['ID_status'].update(error_message)
            filtered_df = df[df['Output_ID'].notna()].drop(0, axis=1)
            row = filtered_df[filtered_df['Output_ID'] == int(ID_reader)].iloc[0]
            info = row.values.tolist()
            Sci.show_info(info)
        elif error_message == 'Daily ticket':
            window['ID_status'].update(error_message)
        img_path = take_picture(ID_reader)
        pld.plate_retrival(img_path)
        lr.log(ws, ID_reader, img_path, lr.check(ID_reader, ws))
window.close()
