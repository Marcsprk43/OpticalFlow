#Imports
from picamera import PiCamera
from time import sleep
import os, sys
import serial

#Setup Functions
name = ""
foldername = ""
ser = serial.Serial('/dev/ttyUSB0', baudrate=115200,
                    bytesize=8, parity='N', stopbits=1,
                    timeout=0.5, xonxoff=0, rtscts=0)

def initialize_camera(cam, camera_settings=None, **kwargs):
    global camera

    camera = PiCamera(**kwargs)
    camera.rotation = 180
    if camera_settings == None:
        print('Calibrating camera settings')
        camera.resolution = (1640,1232)
        camera.start_preview(alpha=255)
        camera.preview.fullscreen = False
        camera.preview.window = (0,0,640,480)
        print('Camera resolution:{}'.format(camera.resolution))
        sleep(5)

        camera_settings = {}
        camera_settings['iso'] = 100
        camera_settings['shutter_speed'] = camera.exposure_speed
        camera_settings['awb_gains'] = camera.awb_gains
        camera_settings['analog_gain'] = camera.analog_gain
        camera_settings['digital_gain'] = camera.digital_gain
        print('Shutter speed: {}'.format(camera_settings['shutter_speed']))
        print('AWB Gains: {}'.format(camera_settings['awb_gains']))
        print('analog_gain: {}'.format(camera.analog_gain))
        print('digital_gain: {}'.format(camera.digital_gain))

    else:
        camera.exposure_mode = 'off'
        camera.awb_mode = 'off'
        camera.iso = camera_settings['iso']
        camera.shutter_speed = camera_settings['shutter_speed']
        camera.awb_gains = camera_settings['awb_gains']
        
    return camera, camera_settings

#Folder Creation
data_dir = ""
def create_Folder(folderName):
    global data_dir
    
    if os.path.exists(folderName) == False:
        os.mkdir(folderName)
    return folderName


HOME = b'$H\n'
RESET_0 = b"G92 X1\n"
STATUS = b'?\n'

def move(pos, speed):
    command = 'G1 X{} F{}\n'.format(pos, speed*60)
    print('Move command: '+command)
    
    ser.write(command.encode('utf-8'))
    status = ser.read(100)
    print("After G0 Command"+str(status))
    position=100
    while abs(position - pos) > 1:
        ser.reset_input_buffer()
        ser.write(STATUS)
        status = ser.readline()
        while str(status)[2] != "<":
            status = ser.readline()
        print(status)
        position = float(status.split(b",")[4].split(b':')[1])
        sleep(0.2)
        
    sleep(0.5)
    

#Picture Defs
def take_video(path, speed, run):


    camera.resolution=(1640,1232)
    fps = 30

    camera.framerate=fps
    camera.start_recording(path+'/Video_{}_{}.h264'.format(speed,run),
                           bitrate=15000000,
                           motion_output=path+'/motion_{}_{}.dat'.format(speed,run))
    #start move
    move(315.0, speed)
    #read grbl status every .5 seconds
    
    #If x==315.000, quit loop
    
    #Stop recording
    camera.stop_recording()

    move(1.0, 80)

       
    print("Finished Loop")
    sleep(2)

settings = {}
camera, settings = initialize_camera("A", camera_settings=None,
                                             resolution=(1640,1232))
camera.start_preview(alpha=200)       
folder = input("Enter Test Name:  ")
create_Folder("/home/pi/data/{}".format(folder))
runs = input("Runs:  ")
speeds = [15,30,45,60,75]
camera.stop_preview()
camera.close()
camera, settings = initialize_camera("A", camera_settings=settings,
                                             resolution=(1640,1232))
ser.write(HOME)
status = ser.read(100)
print("After Home Command"+str(status))
sleep(5)
ser.write(RESET_0)
status = ser.read(100)
print("After 0 Command"+str(status))

for speed in speeds:
    current_folder = create_Folder(("/home/pi/data/{}/Speed_{:03d}".format(folder,speed)))
    for run in range(int(runs)):
        #pictures(inc, numbera, inc, current_folder)
        take_video(current_folder, speed, run)
camera.close()
