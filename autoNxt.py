#!/usr/bin/env python

import nxt
import sys
from time import sleep
import nxt.locator
import tty, termios
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
left = nxt.Motor(brick, PORT_A)
right = nxt.Motor(brick, PORT_C)
usMotor = nxt.Motor(brick, PORT_B)
both = nxt.SynchronizedMotors(left, right, 0)
rightboth = nxt.SynchronizedMotors(left, right, 100)
leftboth = nxt.SynchronizedMotors(right, left, 100)
color = Color20(brick, PORT_2)
us = Ultrasonic(brick, PORT_1)
fronttouch = Touch(brick, PORT_3)
backtouch = Touch(brick, PORT_4)
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
    print "Motor Cam: " + str(usMotor._read_state())
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




#######################################################

status()


print "Ready..."

try:
    while True:
        #ch = getch()
        print "Ultrasonic: ", us.get_distance()
        
        if us.get_distance() < 20 or fronttouch.is_pressed():
            if fronttouch.is_pressed():
                both.turn(100, 90, False) # Backup # Maybe only when TOuched?
                both.brake()
                if backtouch.is_pressed():
                    both.turn(-100, 60, False)
                    both.brake()
            usMotor.turn(100, 90)
            leftUS = us.get_distance()
            usMotor.turn(-100, 180)
            rightUS = us.get_distance()
            usMotor.turn(100, 90)
            if leftUS > rightUS:
                leftboth.turn(-100, 90, False)
                leftboth.brake()
            else:
                rightboth.turn(100, 90, False)
                rightboth.brake()
        else:
            # May be change this to run?
            both.turn(-100, 180, False)   # Forward Unto Dawn
            both.brake()
        
except KeyboardInterrupt:
    print "INTERRUPTED!!"

color.set_light_color(COLORNONE)
sock.close()

print "Finished"
