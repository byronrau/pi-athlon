Overview
This project will be mainly getting the robot put together, testing the sensors and motors, and then putting it all together by using the sensors to track a line to drive the motors.

Robot Test
Turn on the Raspberry Pi and go to home directory 


cd /home/pi 
# should be there by default

cd Adafruit-Motor-HAT-Python-Library/examples

cp RobotTest.py First_project.py
# we want to create a copy so we can “play” with the copy and not change original file 

ls  
# you should now see a file called First_project.py

 nano First_project.py
 # edit this file this file is a copy so we do not mess up the original file RobotTest.py
 # you can use whatever editor you feel most comfortable with  
You can now “play/change” parameters and lines with the First_project.py file to get your Robot to perform different operations relate to the motors and direction. This will help you understand how the First_project.py script controls the motor speed and direction thus controlling the movement of the Robot itself (see below screen shot of First-project.py file). 

Let’s look at first line of the First_project.py file (see screen shot below): 


Robot.forward (150, 1.0) 
The function is robot.forward  (150, 1.0) the 150 is the speed of the motor and the 1.0 is the time for the motor to stay at 150. 

By changing the speed and time you can see how it changes the movement of the robot. The speed is from 0-255 and the time is well the time…. 

Begin playing so you understand the motor scripting and how to manipulate the robot movement and speed. Remember this is a copy so don’t be afraid to change things up you will not corrupt the original file. Think of this as your sandbox. 


How to run your file First_project.py 
Make sure you are at the “Adafruit-Motor-HAT-Python-Library/examples”  directory 


python First_project.py  
# this will execute your file/script
Motor-HAT board pin layout

The above pin out and the pin out below of the Raspberry pi GPIO pins will assists you in determining which pins ( Motor-HAT) connect to which GPIO pins so you can use sensors to control you robot. For our first project you will need to know where you want to pin you Arduino sensor to on the motor-HAT board and program the Raspberry Pi


Line tracking Sensor for our first project. The line tracking sensor consists of three main parts they are: 

The tracking diode 

The potentiometer 

The 3 pins (power, ground, and output) 

You will attach your sensor via standoffs (they with the sensors will be provided to you) to the Robot as seen in the below photo: 


Then connect your sensor wires to power, ground and I/O pins on the Motor-HAT board (see above layout). I would suggest before you connect the sensor wires to the robot that you just put 5volts and ground to the sensor. Then monitor the output pin of the sensor as you cover the tracking diode with a DVM (Digital Volt Meter) to see the voltage swing of the sensor. This will help you “see” how close an object (this case the black tape) needs to be for the sensor to pick it up. You can use the potentiometer to adjust the distance it takes to change states (high (5V) to low (.1V). 

Please see the section Configuring Sensors instead.

Here is a link to assist you in understanding how the sensor and GPIO interact within a script. The link does not use the same tracking sensor as our project but the concept is the same. 

https://diyhacking.com/raspberry-pi-gpio-control/ 

Let’s look at a script to test the sensors: 

Power on your Raspberry Pi 


cd /home/pi
# go to your home directory

cd Adafruit-Motor-HAT-Python-Library/examples
# go to the examples dirctory
Now let’s create a blank file so we can copy and paste a test script to test the sensors 


nano linetrackFunc.py 
# this will create a blank file called linetrackFunc.py
Take the below screen shot and physically type (enter) it into the file you just created above 


2. After entering (typing) the script into the file, save the file by hitting the Ctrl  and O keys then exit Ctrl X (these prompts should be at the bottom of the screen when you are in the file itself) 

Description of script 
What we are doing with this simple script is setting up the GPIO 22 and 27 (pins 15 and 13) to be set as input pins. The “while” loop is looking for a signal from either of the sensors located on the robot through the GPIO ports. 

This script will allow you to visually see on the terminal the changes of voltage on the output pin of the sensor as you pass an object (finger, black tape etc.) under the sensors. 

Now, you have seen how the motors and sensors work as well as the GPIO ports.  Now the fun begins! 

Your task is to write a script that will enable your robot to follow a black line in our cases a solid piece of black tape. 