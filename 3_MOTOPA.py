#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import (Motor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog

from pybricks.hubs import EV3Brick

ev3 = EV3Brick()


import struct

# This program uses the two PS4 sticks to control two EV3 Large Servo Motors using tank like controls

# Create your objects here.
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
steer_motor = Motor(Port.B)
center = 0

left_speed = 0
right_speed = 0

# Locat the event file you want to react to, on my setup the PS4 controller button events
# are located in /dev/input/event4
infile_path = "/dev/input/event4"
in_file = open(infile_path, "rb")


ev3.speaker.set_volume(100)

ev3.speaker.set_speech_options(voice='m1',speed=200, language='ru')

# ev3.speaker.play_file("/home/robot/dualshock/sound/SNEZHNIY.wav")




# Define the format the event data will be read
# See https://docs.python.org/3/library/struct.html#format-characters for more details
FORMAT = 'llHHi'
EVENT_SIZE = struct.calcsize(FORMAT)
event = in_file.read(EVENT_SIZE)

# A helper function for converting stick values (0 to 255) to more usable numbers (-100 to 100)
def scale(val, src, dst):
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

# Create a loop to react to events
while event:

    # Place event data into variables
    (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)

    # If a button was pressed or released
    if ev_type == 1:
        if code == 310 and value == 0:
            steer_motor.reset_angle(steer_motor.angle()-5)
        if code == 311 and value == 0:
            steer_motor.reset_angle(steer_motor.angle()+5)

        if code == 310 and (value == 0 or value == 1):
            center = scale(-1, (0,255), (40, -40))
        if code == 311 and (value == 0 or value == 1):
            center = scale(1, (0,255), (40, -40))

        # ev3.speaker.say(str(code))

        # ev3.speaker.beep()

        # ev3.speaker.say(str(value))
    
    elif ev_type == 3: # Stick was moved
        
        # React to the left stick
        if code == 1:
            left_speed = scale(value, (0,255), (100, -100))
        
        # React to the right stick
        if code == 4:
            right_speed = scale(value, (0,255), (100, -100))
        # if value < 120:
        #     print('code='+ str(code) +'  value=' + str(value))
        if code == 17:
             print('code='+ str(code) +'  value=' + str(value))
             steer_motor.dc((-value * 100))
            
                
    # Set motor speed
    left_motor.dc(left_speed)
    right_motor.dc(right_speed)

     # Track the steering angle
    # steer_motor.track_target(center)

    # Read the next event
    event = in_file.read(EVENT_SIZE)

in_file.close()