"""Project 1 pi-athlon

This project is intended to have the pi-athlon follow a line and self drive
itself along a track.

"""

#!/usr/bin/python

import RPi.GPIO as GPIO
import Robot

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
chan_list = [13,16]
GPIO.setup(13, GPIO.IN)
GPIO.setup(16, GPIO.IN)

LEFT_TRIM   = 0
RIGHT_TRIM  = 0

robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)


while True:
    RIGHT_SENSOR = GPIO.input(13)
    LEFT_SENSOR = GPIO.input(16)

    if (RIGHT_SENSOR == 1) and (LEFT_SENSOR == 0):
        robot.right(40)
        continue

    if (LEFT_SENSOR == 1) and (RIGHT_SENSOR == 0):
        robot.left(40)
        continue

    if (RIGHT_SENSOR == 1) and (LEFT_SENSOR == 1):
        robot.forward(90)
        continue


    if (RIGHT_SENSOR == 0) and (LEFT_SENSOR == 0):
        robot.backward(40)
        continue
 