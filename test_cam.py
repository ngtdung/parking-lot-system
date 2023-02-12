import time
from picamera2 import Picamera2, Preview

def take_picture(id, row_val):
    picam = Picamera2()
    config = picam.create_still_configuration(main={'size':(1920, 1080)}, lores={'size': (640,480)}, display='lores')
    picam.configure(config)

    picam.start_preview(Preview.QTGL)

    picam.start()
    time.sleep(2)
    now = time.localtime()
    path = str(id) + time.strftime('%H%M%S', now)
    if row_val > 0:
        path_complete = "/logout_images/{}.jpg".format(path)
    else:
        path_complete = "/login_images/{}.jpg".format(path)
    picam.capture_file(path_complete)
    picam.close()
    return(path_complete)


