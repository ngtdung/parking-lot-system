import PySimpleGUI as sg
from subprocess import *
sg.theme('LightBlue')

layout = [
    [sg.Button('Create monthly ticket', key= "create"),
     sg.Button('Scan ticket', key= "scan"),
     sg.Button('Delete Card', key='delete')]
]

window = sg.Window('RFID', layout)

while True:
    event, values = window.read()
    if event == 'create':
        call('python', 'GUI.py')
    elif event == 'scan':
        call('python', 'scan_ID_to_info.py')
    elif event == 'delete':
        call('python', 'Delete_RFID.py')
window.close()