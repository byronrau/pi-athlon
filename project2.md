Overview
In this project you will build upon your first project (follow a black line) by incorporating multiple sensor within your Python script.  The sensors involved with this project are as follows, see parts audit for project to view each sensor:

Temperature sensor

Obstacle avoidance sensor

Sound device (buzzer)

3RGB-LED device

Objective 1

Your robot will follow a black line and the 3RGB-LED will remain on and green and as your sensors/devices encounter positive inputs the robot will perform varies actions. The robot will encounter an object along its path and the obstacle avoidance sensor will exhibit a positive trigger which will cause the robot to stop. When the robot stops the 3RGB-LED will turn red and when 5 seconds has elapsed the sound device (buzzer) will be activated producing a "buzzing" sound. The sound will remain until the obstacle is moved at which point the sound device will deactivate turning off the "buzzing" sound and the 3RGB-LED will turn green and the robot will begin following (moving down) the black line as before. 

Objective 2

The next encounter will be with the temperature sensor, the temperature sensor will detect a heat source ( a temperature that exceeds 28 degrees Celsius this is the threshold) at which point the robot will stop and the 3RGD-LED will turn blue. The robot will remain stopped for an elapsed time of 10 seconds. After 20 seconds the robot will begin following the black line once again and the 3RGB-LED will once again turn green. When the robot has completed the above states successfully this 2nd project will be completed. 

Support information on sensors
There is an overall description for each sensor made by the manufacturer the link can be found here:

https://www.sunfounder.com/learn/category/Sensor-Kit-v1-0-for-Raspberry-Pi.html

This link has the description information for all of their sensors. We will only be interested in 4 of these sensors for this project and they are:

Lesson 2 RGB LED 

Lesson 11 Buzzer

Lesson 22 Obstacle Avoidance Sensor

Lesson 17 DS18B20 Temperature Sensor - Be sure to see the Tips and Tricks section for more information on getting this sensor configured.

Just go to the above link find the sensor lesson and read about the sensor. This will provide you with all the information needed to get started.

Hardware installation
I have provided pictures of where each sensor should go and how they should be attached to the Robot chassis simply follow along.





Let me know if you have any questions. Good luck and have fun!!!

Tips and Tricks
Tip #1 - Configuring the Temperature Sensor

Here are the pre-configuration steps to get the temperature sensor operational.

Make sure you plug in the temperature sensor signal into GPIO4 pin (it is the 5th one from the left following the GPIO Mapping)

Make a small change to the config.txt file using:


sudo nano /boot/config.txt
add the following line to the bottom, if not already there


dtoverlay=w1-gpio,gpiopin=4
The device is setup to report its temperature via the GPIO4 pin.

Reboot the Raspberry Pi.

Mount the temperature sensor (you should only have to do this once)


# mount device
sudo modprobe w1-gpio
sudo modprobe w1-therm
then navigate to the following directory:


cd /sys/bus/w1/devices
ls
This will list the directories associated with the temperature sensor. Each one has a unique ID and in my case it is 28-00000482b243. Your ID will be different so be sure to use that in the example code below. Using cd you can change to the temperature sensor directory, list the contents and then view the w1_slave file :


cd 28-00000482b243
ls
cat w1_slave

The w1_slave file contains a bunch of data but the “t=23062” at the end is the temperature reading. The temperature is read as 23062/1000 =  23.062 degrees Celsius.

Note: To convert to Fahrenheit,  the formula is 23.062 * 1.8 + 32 =  73.5 degrees. or F = C * 9/5 + 32.

Tip #2 - RGB Hex Values

red = 0x00FFFF
green = 0xFF00FF
blue = 0xFFFF00

# these correspond to my pins I'ved inserted the RGB sensors to, yours may be different
rgb_pins = {"pin_R": 35, "pin_G": 38, "pin_B": 40}

# init rgb
for pin in rgb_pins:
    # Set pins' mode is output
    GPIO.setup(rgb_pins[pin], GPIO.OUT)
    # Set pins to high to off led
    GPIO.output(rgb_pins[pin], GPIO.HIGH)

# set Frequece to 2KHz
p_R = GPIO.PWM(rgb_pins['pin_R'], 2000)
p_G = GPIO.PWM(rgb_pins['pin_G'], 2000)
p_B = GPIO.PWM(rgb_pins['pin_B'], 2000)

# Initial duty Cycle = 0(leds off)
p_R.start(0)
p_G.start(0)
p_B.start(0)

def map_rgb(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setColor(col):
    R_val = (col & 0xff0000) >> 16
    G_val = (col & 0x00ff00) >> 8
    B_val = (col & 0x0000ff) >> 0

    R_val = map_rgb(R_val, 0, 255, 0, 100)
    G_val = map_rgb(G_val, 0, 255, 0, 100)
    B_val = map_rgb(B_val, 0, 255, 0, 100)

    # Change duty cycle
    p_R.ChangeDutyCycle(R_val)
    p_G.ChangeDutyCycle(G_val)
    p_B.ChangeDutyCycle(B_val)
    
# now to set the color you can just call the function
setColor(blue)
You can use the following hex values for red, green and blue colors for the RGB LED.

Tip #3 - Reading the temp sensor during loop causing robot to go off track
You may find that reading the temp sensor during the main robot loop causes the robot to go off track. One possible solution for this, is not read the temp sensor output file on every iteration of the loop but instead only read it periodically (every x number of seconds instead). An example implementation do this:


import time

def read_sensor():
    # reads the temp sensor file and returns the temp value as int

def loop():
    # initialize the start time to be current time
    start_time = time.time()
    # main robot loop
    while True:
        # if the current time is greater than start_time + 5s, check sensor
        # 5s is just an example you can try other values depending on robot responsiveness
        if time.time() > start_time + 5:
            # reset start time to current time
            start_time = time.time()
            # reads the temp sensor value from temp sensor output file
            temp = read_sensor()
            # the temp value will depend on your heat source and ambient temp values
            # so adjust as needed for your environment
            if temp > 30000:
                setColor(blue)
                GPIO.output(buzzer_pin, GPIO.LOW)
                robot.stop()
                time.sleep(20)
            else:
                setColor(green)
                GPIO.output(buzzer_pin, GPIO.HIGH)
        
        # continue checking other sensors
Tip #4 - Use the +5v for the sensors
Despite what some of the schematics say in the documentation you can use the +5v for the sensors if you are not getting proper output from the sensors.