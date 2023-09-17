from picamera import PiCamera
from time import sleep
import RPi.GPIO as gp
import os
import cv2

A = {7:False, 11:False, 12:True, 'i2c':4}
B = {7:True, 11:False, 12:True, 'i2c':5}
C = {7:False, 11:True, 12:False, 'i2c':6}
D = {7:True, 11:True, 12:False, 'i2c':7}

camera = None

def initialize_camera():
    global camera
    
    gp.setwarnings(False)
    gp.setmode(gp.BOARD)
    gp.setup(7, gp.OUT)
    gp.setup(11, gp.OUT)
    gp.setup(12, gp.OUT)

    gp.setup(15, gp.OUT)
    gp.setup(16, gp.OUT)
    gp.setup(21, gp.OUT)
    gp.setup(22, gp.OUT)
    
    i2c = "i2cset -y 1 0x70 0x00 0x04"
    
    os.system(i2c)
    select_camera(A)
    camera = PiCamera()
    camera.rotation = 180
    return camera

def select_camera(cam):
    i2c = "i2cset -y 1 0x70 0x00 0x0{}".format(cam['i2c'])
    os.system(i2c)
    gp.output(7, cam[7])
    gp.output(11, cam[11])
    gp.output(12, cam[12])
    
    
def capture_stereo(folder, file_number):
    global camera
    

    #camera.capture('{}/StereoImage_{}_A.png'.format(folder, file_number))
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format='bgr')
        # At this point the image is available as stream.array
        image = stream.array
        cv2.imwrite('{}/StereoImage_{}_A.bgr'.format(folder, file_number), image)
    camera.stop_preview()

    select_camera(C)

    camera.start_preview(alpha=250)
    sleep(3)
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format='bgr')
        # At this point the image is available as stream.array
        image = stream.array
        cv2.imwrite('{}/StereoImage_{}_C.bgr'.format(folder, file_number), image)
    camera.stop_preview()
    
def main():
    global camera

    print("Setting up Arducam...", end='')
    camera = initialize_camera()
    print("Done!")
    
    folder = '/home/pi/data/CalibrationLeftRight'
    if not os.path.exists(folder):
        print('Creating new folder: {}'.format(folder))
        os.makedirs(folder)


    select_camera(A)
    camera.start_preview(alpha=230)   
    wait(5)

    for i in range(40):
        select_camera(A)
        camera.start_preview(alpha=200)
        temp = input("Press any key to capture")        
        capture_stereo(folder, i)


if __name__ == "__main__":
    main()


