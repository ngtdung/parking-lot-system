# Import libraries
import time
from picamera2 import Picamera2, Preview


def take_picture(id, row_val): # Take picture using raspberry's camera module
    picam = Picamera2() # Initialize camera
    config = picam.create_still_configuration(main={'size': (1920, 1080)}, lores={'size': (640, 480)}, display='lores') # Image configuration
    picam.configure(config)
    picam.start_preview(Preview.QTGL) # Open the preview window for 3 seconds
    picam.start()
    time.sleep(3)
    now = time.localtime() # Get time when picture was taken
    path = str(id) + time.strftime('%H%M%S', now) # Format the time into the image saved
    if row_val > 0:
        path_complete = "/logout_images/{}.jpg".format(path) # Save into logout folder
    else:
        path_complete = "/login_images/{}.jpg".format(path) # Save into login folder
    picam.capture_file(path_complete) # Save image
    picam.close()
    return path_complete # Return image path
