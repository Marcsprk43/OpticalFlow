from picamera import PiCamera
from time import sleep
import RPi.GPIO as gp
import os

A = {7:False, 11:False, 12:True, 'i2c':4, 'name':'A'}
B = {7:True, 11:False, 12:True, 'i2c':5, 'name':'B'}
C = {7:False, 11:True, 12:False, 'i2c':6, 'name':'C'}
D = {7:True, 11:True, 12:False, 'i2c':7, 'name':'D'}

camera = None

def initialize_camera():
    global camera
#    camera = PiCamera()
    camera = PiCamera(sensor_mode=1,resolution=(1920,1080))
    camera.rotation = 180
    return camera


    
def capture_single_camera(num_pic, folder, format='png'):
    global camera
    


    camera.start_preview(alpha=230)
    sleep(2)
    for pic in range(40):
        camera.capture('{}/CalibrationImage_{:03d}_{}.{}'
                       .format(folder, pic, 'Optical_Flow_Camera',format),format=format)
    camera.stop_preview()   
    
    
    
def main():
    global camera

    print("Setting up Arducam...", end='')
    camera = initialize_camera()
    print("Done!")
    
    folder = '/home/pi/data/Calibration_Optical_Flow'
    if not os.path.exists(folder):
        print('Creating new folder: {}'.format(folder))
        os.makedirs(folder)
    camera.start_preview(alpha=230)
    sleep(5)    
    capture_single_camera(40, folder, format='png')

if __name__ == "__main__":
    main()

