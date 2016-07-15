#!/usr/bin/env python
#
 
import nxt
import sys
import tty, termios
from time import sleep
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
rightboth = nxt.SynchronizedMotors(left, right, 100)
leftboth = nxt.SynchronizedMotors(right, left, 100)
color = Color20(brick, PORT_2)
us = Ultrasonic(brick, PORT_1)
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
    print 'Color: ', color.get_sample()    
    print 'Ultrasonic: ', us.get_sample()  
    color.set_light_color(COLORNONE)
    print "All Sensors accounted for..."


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
    print "q - CAMERA MOTOR UP"
    print "e - CAMERA MOTOR DOWN"
    print "l - LIGHT TOGGLE"
    print "u - ULTRASONIC SENSOR"
    print "o - OBSERVE REFELCTED LIGHT"
    print "h - HELP"


#######################################################

status()

ch = ' '
print "Ready..."
while ch != '~':
    ch = getch()
 
    if ch == 'w': # Add Ultrasonic check here for maybe 10
        print "Forwards"
        both.turn(-100,180, False)
        both.brake()
    elif ch == 's': # Add Ultrasonic check here for maybe 10
        print "Backwards"
        both.turn(100,180, False)
        both.brake()
    elif ch == 'a':
        print "Left"
        leftboth.turn(-100,90,False)
        leftboth.brake()
    elif ch == 'd':
        print "Right"
        rightboth.turn(100,90,False)
        rightboth.brake()
    elif ch == 'q':
        print "Camera Mtr Up"
        cameraMtr.turn(90, 60) #Test angle, maybe reduce
    elif ch == 'e':
        print "Camera Mtr Down"
        cameraMtr.turn(-90, 60) # Test agnle, maybe reduce
    elif ch == 'l':
        changeColor()
    elif ch == 'h':
        usage()
    elif ch == 'u':
        print 'Ultrasonic: ', us.get_distance()
    elif ch == 'o':
        print "Reflected Light: " + str(color.get_color()) 

        
color.set_light_color(COLORNONE)
sock.close()

print "Finished"
