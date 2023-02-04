import tkinter as tk

def scan_rfid():
    # Code to read the ID from the RFID card using the RC522 module
    rfid_id = '1234567890'

    # Display the RFID ID on the screen
    label.config(text='RFID ID: ' + rfid_id)
    return rfid_id

# Create the GUI window
root = tk.Tk()

root.title("RFID Scanner")

# Create the button to scan the RFID card
scan_button = tk.Button(root, text="Scan RFID", command=scan_rfid)
scan_button.pack()

create_profile_button = tk.Button(root, text='Create new card')
create_profile_button.pack()

# Create the label to display the RFID ID
label = tk.Label(root, text="")
label.pack()

# Start the GUI event loop
root.mainloop()
