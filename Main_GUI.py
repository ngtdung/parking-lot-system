import PySimpleGUI as sg
from subprocess import call

sg.theme('LightBlue')

layout = [
    [sg.Button('Create monthly ticket', key= "create"), sg.Button('Scan ticket', key= "scan")]
]

window = sg.Window('RFID', layout)

while True:
    event, values = window.read()
    if event == 'create':
        call('python', 'GUI.py')
    elif event == 'scan':
        call('python', 'scan_ID_to_info.py')

window.close()