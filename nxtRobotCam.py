#!/usr/bin/env python
#
 
import nxt
import sys
import tty, termios
from time import sleep
from picamera import PiCamera
import nxt.locator
from nxt.sensor import *
from nxt.motor import *
from nxt.bluesock import BlueSock


COLORFULL = 0x0D  
COLORRED = 0x0E 
COLORGREEN = 0x0F 
COLORBLUE = 0x10
COLORNONE = 0x11  
COLOREXIT = 0x12  


ID = "00:16:53:11:18:20"

sock = BlueSock(ID)
brick = sock.connect()
left = nxt.Motor(brick, PORT_A) # Maybe A
right = nxt.Motor(brick, PORT_C)
cameraMtr = nxt.Motor(brick, PORT_B)
both = nxt.SynchronizedMotors(left, right, 0)
leftboth = nxt.SynchronizedMotors(left, right, 100)
rightboth = nxt.SynchronizedMotors(right, left, 100)
color = Color20(brick, PORT_2)
us = Ultrasonic(brick, PORT_1)
camera = PiCamera()
photoCount = 0
vidCount = 0
colorMode = 0

"""
Gets character
"""
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
 

"""
Inital Setup Check
"""
def status():
    print "Sock Status: " + str(sock)
    print "Motor Left: " + str(left._read_state())
    print "Motor Right: " + str(right._read_state())
    print "Motor Cam: " + str(cameraMtr._read_state())
    print 'Color: ', color.get_sample()    # use set_light_color(col), get_light_color(), get_reflected_light(), get_color()
    print 'Ultrasonic: ', us.get_sample()  # use get_distance()
    #print 'Touch 1: ', Touch(brick, PORT_3).get_sample(), is_pressed()
    #print 'Touch 2: ', Touch(brick, PORT_4).get_sample()
    #Many sensore get_sample is equivalent to getters for sensors.
    color.set_light_color(COLORNONE)
    print "All Sensors accounted for..."


"""
Camera Methods

### Add LED Indicators from COLOR sensor to indicate modes!!!!!!
"""
def capture():
    global photoCount
    camera.resolution = (2592,1944)
    camera.framerate = 15
    col = color.get_light_color()
    color.set_light_color(COLORRED)
    camera.start_preview()
    sleep(3)
    camera.capture('/home/pi/Desktop/Pics/Images/image%s.jpg' % photoCount) # change to timestamp
    photoCount += 1
    camera.stop_preview()
    color.set_light_color(col)

def burstCapture():
    global photoCount
    camera.resolution = (2592,1944)
    camera.framerate = 15
    col = color.get_light_color()
    color.set_light_color(COLORRED)
    camera.start_preview()
    for i in range(5):
        sleep(2)
        camera.capture('/home/pi/Desktop/Pics/Images/image%s.jpg' % photoCount) # change to time stamp
        photoCount += 1
    camera.stop_preview()
    color.set_light_color(col)

def video():
    global vidCount
    camera.resolution = (1920,1080)
    camera.framerate = 15
    col = color.get_light_color()
    color.set_light_color(COLORRED)
    camera.start_preview()
    camera.start_recording('/home/pi/Desktop/Pics/Video/video%s.h264' % vidCount) # change to time stamp
    vidCount += 1
    sleep(10)
    camera.stop_recording()
    camera.stop_preview()
    color.set_light_color(col)

"""
Toggles Light Sensor's color
"""
def changeColor():
    global colorMode
    colorMode += 1
    stat = colorMode % 5
    if stat == 0:
        print "Light Toggle, Color Mode: OFF"
        color.set_light_color(COLORNONE)
    elif stat == 1:
        print "Light Toggle, Color Mode: FULL"
        color.set_light_color(COLORFULL)
    elif stat == 2:
        print "Light Toggle, Color Mode: RED"
        color.set_light_color(COLORRED)
    elif stat == 3:
        print "Light Toggle, Color Mode: GREEN"
        color.set_light_color(COLORGREEN)
    elif stat == 4:
        print "Light Toggle, Color Mode: BLUE"
        color.set_light_color(COLORBLUE)

"""
Usage Guidelines
"""
def usage():
    print "~ - QUIT"
    print "w - MOVE FORWARD"
    print "s - MOVE REVERSE"
    print "a - MOVE LEFT"
    print "d - MOVE RIGHT"
    print "v - VIDEO CAPTURE"
    print "b - CAMERA BURST"
    print "c - CAMERA CAPTURE"
    print "q - CAMERA MOTOR UP"
    print "e - CAMERA MOTOR DOWN"
    print "l - LIGHT TOGGLE"
    print "u - ULTRASONIC SENSOR"
    print "o - OBSERVE REFELCTED LIGHT"
    print "h - HELP"


#####################################################33

status()

ch = ' '
print "Ready"
while ch != '~':
    ch = getch()
 
    if ch == 'w': # Add Ultrasonic check here for maybe 10
        print "Forwards"
        both.turn(-100, 180, False)
    elif ch == 's': # Add Ultrasonic check here for maybe 10
        print "Backwards"
        both.turn(100, 180, False)
    elif ch == 'a':
        print "Left"
        leftboth.turn(-50, 90, False)
    elif ch == 'd':
        print "Right"
        rightboth.turn(50, 90, False)
    elif ch == 'v':
        print "Video Capture"
        video()
    elif ch == 'b':
        print "Camera Burst"
        burstCapture()
    elif ch == 'c':
        print "Camera Capture"
        capture()
    elif ch == 'q':
        print "Camera Mtr Up"
        cameraMtr.turn(50, 60) #Test angle, maybe reduce
    elif ch == 'e':
        print "Camera Mtr Down"
        cameraMtr.turn(-50, 60) # Test agnle, maybe reduce
    elif ch == 'l':
        changeColor()
    elif ch == 'h':
        usage()
    elif ch == 'u':
        print 'Ultrasonic: ', us.get_distance()
    elif ch == 'o':
        print "Reflected Light: " + str(color.get_color()) # Add Interpretation for reflected light

        
color.set_light_color(COLORNONE)
sock.close()

print "Finished"
