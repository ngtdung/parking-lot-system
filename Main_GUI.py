import PySimpleGUI as sg
from subprocess import *


sg.theme('LightBlue')

layout = [
    [sg.Button('Create monthly ticket', key= "create_mtl"),
     sg.Button('Entry/Exit Scan', key= 'create_daily')],
     [sg.Button('Scan ticket', key= "scan"),
     sg.Button('Delete Card', key='delete')]
]

window = sg.Window('RFID', layout, resizable=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'create_mtl':
        call(['python', 'RFID.py'])
    elif event == 'scan':
        call(['python', 'scan_ID_to_info.py'])
    elif event == 'delete':
        call(['python', 'Delete_RFID.py'])
    elif event == 'create_daily':
        call(['python', 'scan_to_log.py'])

window.close()