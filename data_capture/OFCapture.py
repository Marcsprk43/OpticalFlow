#Imports
from time import sleep
import os, sys
import serial
import json
import math
import string
import random


# Experimental setup parameters
slideL = 314
rotDeg = 30

camera_h = 3264
camera_v = 2464
camera_fps = 21


running_on = "Nano"  # this should be "Mac" or "Nano"

rootdatadir = '/home/sparky/Documents/data/'

#Variable
mmPerSec = 30
degPerSec = 8


#Setup Functions
name = ""
foldername = ""


def initialize_camera(cam, camera_settings=None, **kwargs):
    print('Camera initialization here....')
    return 0


#Folder Creation
data_dir = ""
def create_Folder(folderName):
    
    if os.path.exists(folderName) == False:
        os.mkdir(folderName)
    return folderName

# Gcode movement functions
def home_x(status=True, print_status=True):
    return send_gcode('G28 X', status=status, print_status=print_status)

def set_xy_pos(x_pos, y_pos, status=True, print_status=True):
    return send_gcode('G92 X{} Y{}'.format(x_pos, y_pos), status=status, print_status=print_status)

def disable_y_stepper(status=True, print_status=True):
    return send_gcode('M18 Y', status=status, print_status=print_status)

def get_status(status=True, print_status=True):
    return send_gcode('?', status=status, print_status=print_status)

def move(x_pos, y_pos, feedrate, status=True, print_status=True):
    feed_mm_per_min = feedrate*60
    return send_gcode('G1 X{} Y{} F{}'.format(x_pos, y_pos, feed_mm_per_min), status=status, print_status=print_status)

def pause_ms(ms, status=True, print_status=True):
    return send_gcode('G4 P{}'.format(ms), status=status, print_status=print_status)
   
def send_gcode(command, status=False, print_status=False):
    global ser
    ser.reset_input_buffer()
    command = command +'\n'
    ser.write(command.encode('utf-8'))

    if status:
        stats = ser.read(100) 
        if print_status:
            print(stats)
        return stats
    else:
        return

# experimental movement calculations
def slide_calc(mmPerSec, degPerSec, slideL=314, rotDeg=30 ):
    
    # one of the two will be limiting factor, find which one
    # protect /0
    if mmPerSec == 0.:       
        slide_time = 1e6
    else:
        slide_time = abs(slideL/mmPerSec)
        
    if degPerSec == 0. :
        rotate_time = 1e6
    else:
        rotate_time = abs(rotDeg/degPerSec)
    
        
    if slide_time >= rotate_time:  # this means that the rotation is the limiting factor
        # use the full rotational travel
        rotate_start = -1.0 * math.copysign(1.0,degPerSec) * rotDeg/2
        rotate_end = math.copysign(1,degPerSec) * rotDeg/2
        # reduce the linear travel to fit into the allocated time
        slide_start = -1.0 * rotate_time*mmPerSec/2
        slide_end = rotate_time*mmPerSec/2
        exp_time = rotate_time
        
    elif slide_time < rotate_time:  # this means that linear is the limiting factor
        # use the full linear travel
        slide_start = -1.0 * math.copysign(1.0,mmPerSec) * slideL/2
        slide_end = math.copysign(1,mmPerSec) * slideL/2
        # reduce the angle rotation to fit into the time
        rotate_start = -1.0 * slide_time*degPerSec/2
        rotate_end = slide_time*degPerSec/2
        exp_time = slide_time
        
    # in Gcode the speed is the feedrate^2 = x_feedrate^2 + y_feedrate^2 
    feedrate = math.sqrt(mmPerSec*mmPerSec + degPerSec*degPerSec)

    movement = {'slide_start':slide_start, 'slide_end':slide_end, 'slide_speed':mmPerSec,
                'rotate_start':rotate_start, 'rotate_end':rotate_end, 'rotate_speed':degPerSec,
                'feedrate':feedrate, 'exp_time':exp_time}

    print(movement)
    
    return movement


def json_dump(lista, file):
    with open(file, "w") as out:
        json.dump(lista, out)
def json_read(file):
    with open(file) as json_file:
        return json.load(json_file)

#Picture Defs
def take_video(path, speed, run):
    print('Starting video capture.....')
    return


def create_file_name(experiment_name, linear_speed, rotation_speed, run_number):

    # create filename XXXXXX-GH45RU.mp4  XXXXXXX-GH45RU.json
    letters = string.ascii_uppercase + string.digits
    file_suffix = ''.join(random.choice(letters) for i in range(6)) 

    file_name = ('{}_{}_{}-{}-{}'.format(experiment_name,
                                        linear_speed,
                                        rotation_speed,
                                        run_number,
                                        file_suffix))

    return file_name



ser = None


def main():
    global ser

    try:
        if running_on == 'Nano':
            serial_port = '/dev/ttyUSB0'

        elif running_on == 'Mac':
            serial_port = '/dev/cu.usbserial-14110'

        else:
            print('Unknown value or "running_on" variable: {}'.format(running_on))
            exit()

        ser = serial.Serial(serial_port, baudrate=115200,
                                bytesize=8, parity='N', stopbits=1,
                                timeout=0.5, xonxoff=0, rtscts=0)
    except:
        print('Error connecting to serial port {}'.format(serial_port))
        exit()


    test_type = ' '

    while test_type[0] not in ['a', 'm']:
        input_str = input("Auto or Manual experiment [A]/M:")
        
        test_type = input_str.lower()


    if test_type == 'a':
        config_file_name = input("Enter config filename [.json]:")
        if config_file_name[-5:] != '.json':
            config_file_name = config_file_name+'.json'

        # read input file
        try:
            with open(config_file_name) as json_file:
                exp_config = json.load(json_file)
                
        except:
            print('Error opening file {}.... exiting'.format(config_file_name))
            exit()

        datafolder = rootdatadir + exp_config['subfolder'].strip()
        exp_config['datafolder'] = datafolder

        
    else: 
        exp_name = input("Enter experiment name:")
        angular_velocity = float(input('Enter camera angular velocity (deg/s):'))
        linear_velcocity = float(input('Enter camera linear velocity (mm/s):'))
        number_runs = int(input('Enter number of runs:'))
        subfolder = input('Enter subfolder to path: ({})'.format(rootdatadir)) 

        exp_config = {  'slide_speed': linear_velcocity,
                        'rotate_speed': angular_velocity,
                        'exp_name': exp_name,
                        'datafolder':datafolder,
                        'subfolder':subfolder, 
                        'number_runs': number_runs}

    

    if not os.path.exists(exp_config['datafolder']):
        os.mkdir(exp_config['datafolder'])

    if not exp_config['datafolder'][-1] == '/':
        exp_config['datafolder'] = exp_config['datafolder'] + '/'

  
    # check for lists or floats 
    if isinstance(exp_config['rotate_speed'], (int, float)):
        angular_vel_list = [exp_config['rotate_speed']]
    elif not isinstance(exp_config['rotate_speed'], list):
        print('Error angular velocity is not a list float or int - type:{}'.format(type(exp_config['rotate_speed'])))
        exit()
    else:
        angular_vel_list = exp_config['rotate_speed']
   
    
    if isinstance(exp_config['slide_speed'], (int, float)):
        linear_vel_list = [exp_config['slide_speed']]
    elif not isinstance(exp_config['slide_speed'], list):
        print('Error angular velocity is not a list float or int - type:{}'.format(type(exp_config['slide_speed'])))
        exit()
    else:
        linear_vel_list = exp_config['slide_speed']

    print('Angular_vel_list {}'.format(angular_vel_list))
    print('Linear_vel_list {}'.format(linear_vel_list))

    # Calibrate home
    input_str = input('Press enter to start homing sequence....')
    home_x(status=False, print_status=False)
    set_xy_pos(-slideL/2, 0, status=True, print_status=False)
    move(0, 0, 100, status=True, print_status=True)
    disable_y_stepper()
    input_str = input('Rotate camera to zero position')

    input_str = input('Press enter to start experiment....')
    
    for linear_vel in linear_vel_list:

        for angular_vel in angular_vel_list:

            # calculate the movement parameters
            param = slide_calc(linear_vel, angular_vel, slideL=slideL, rotDeg=rotDeg )

            #print(param)
            #sys.exit()

            param['exp_name'] = exp_config['exp_name']
            param['datafolder'] = exp_config['datafolder']
            if test_type == 'a':
                param['exp_config_file'] = config_file_name
            else:
                param['exp_config_file'] = 'manual'
            
            param['camera_h'] = camera_h
            param['camera_v'] = camera_v
            param['camera_fps'] = camera_fps

            for run in range(exp_config['number_runs']):

                print('Run: {}\tLinearV: {}\tAngularV: {}'.format(run, linear_vel, angular_vel))

                # create the custom file name
                file_name = create_file_name(exp_config['exp_name'], linear_vel, angular_vel, run)
                print('Filename is : {}'.format(file_name))
                param['datafile'] = '{}{}.mp4'.format(param['datafolder'],file_name)
                # save the metadata file
                json_dump(param, '{}{}.json'.format(rootdatadir,file_name))


        
        
                # move to starting position at 250mm/s
                move(param['slide_start'], param['rotate_start'], 250)

                sleep(2)

                # start motion with delay
                pause_ms(1000, status=False, print_status=True)

                move(param['slide_end'], param['rotate_end'], param['feedrate'])



                # open video file save to '{}{}.mp4'.format(datafolder,file_name)
                raw_frame_command = ("gst-launch-1.0 -e nvarguscamerasrc num-buffers={} exposuretimerange='500 500' "+
                                "! 'video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1' "+
                                "!  nvv4l2h265enc bitrate=7000000 "+
                                "! h265parse ! qtmux ! filesink location={} -e")
                frame_command = raw_frame_command.format(int(camera_fps*(param['exp_time']+2.)), param['datafile'])
                os.system(frame_command)

                print('\a')
                
          

    print("Going home!!!")
    move(0, 0, 100, status=False, print_status=True) 
    sleep(4)  

      
    print('\a')
        
        


if __name__ == '__main__':
    main()
