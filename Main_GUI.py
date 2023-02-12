# Import necessary libraries
import PySimpleGUI as sg
from subprocess import *


sg.theme('LightBlue') # Set theme for GUI

layout = [
    [sg.Button('Create monthly ticket', key= "create_mtl"),
     sg.Button('Entry/Exit Scan', key= 'create_daily')],
     [sg.Button('Scan ticket', key= "scan"),
     sg.Button('Delete Card', key='delete')]
] # Set layout for GUI

window = sg.Window('RFID', layout, resizable=True) # Initialize main GUI window

while True:
    event, values = window.read() # Track events
    if event == sg.WIN_CLOSED: # Terminate the program when the window is closed
        break
    elif event == 'create_mtl': # Create monthly ticket by linking to RFID.py file
        call(['python', 'RFID.py'])
    elif event == 'scan': # Scan for info of a ticket by linking to scan_ID_to_info.py
        call(['python', 'scan_ID_to_info.py'])
    elif event == 'delete': # Delete a profile from monthly tickets
        call(['python', 'Delete_RFID.py'])
    elif event == 'create_daily': # Record entry/exit of a vehicle
        call(['python', 'scan_to_log.py'])

window.close()