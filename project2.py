"""Project 2 pi-athlon

This project is intended to have the pi-athlon follow a line and self drive
itself along a track. Also adds temperate sensor reading and buzzer for
object detection.

"""

import time
import RPi.GPIO as GPIO
import Robot

RIGHT_PIN = 13
LEFT_PIN = 16
BUZZER_PIN = 15
OBSTACLE_PIN = 18
RGB_PINS = {"pin_R": 35, "pin_G": 38, "pin_B": 40}
RED = 0x00FFFF
GREEN = 0xFF00FF
BLUE = 0xFFFF00
TEMP = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(RIGHT_PIN, GPIO.IN)
GPIO.setup(LEFT_PIN, GPIO.IN)

LEFT_TRIM = 0
RIGHT_TRIM = 0

robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

# rgb
for _, pin in RGB_PINS.items():
    # Set pins' mode is output
    GPIO.setup(RGB_PINS[pin], GPIO.OUT)
    # Set pins to high(+3.3V) to off led
    GPIO.output(RGB_PINS[pin], GPIO.HIGH)

# set Frequece to 2KHz
p_R = GPIO.PWM(RGB_PINS['pin_R'], 2000)
p_G = GPIO.PWM(RGB_PINS['pin_G'], 2000)
p_B = GPIO.PWM(RGB_PINS['pin_B'], 2000)

# Initial duty Cycle = 0(leds off)
p_R.start(0)
p_G.start(0)
p_B.start(0)


def read_sensor():
    """Read sensor

    Returns:
        int: Temp read from sensor
    """
    with open("/sys/bus/w1/devices/28-0314979462d3/w1_slave", "r", encoding="utf-8") as input_file:
        try:
            lines = input_file.readlines()
            temp = lines[-1].split("t=")[1].strip()
            return int(temp)
        except IndexError as exception_name:
            print("Unable to get temp")
            print(exception_name)
            return 0


def setup():
    """Setup buzzer pins
    """
    # buzzer
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    # obstacle
    GPIO.setup(OBSTACLE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def map_rgb(x_val, in_min, in_max, out_min, out_max):
    """Sets the RGB values for ligh

    Args:
        x (int): x value
        in_min (int): input min
        in_max (int): input max
        out_min (int): output min
        out_max (int): output max
    """
    return (x_val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def set_color(color_str):
    """Sets color

    Args:
        color_str (str): name of color
    """
    r_val = (color_str & 0xff0000) >> 16
    g_val = (color_str & 0x00ff00) >> 8
    b_val = (color_str & 0x0000ff) >> 0

    r_val = map_rgb(r_val, 0, 255, 0, 100)
    g_val = map_rgb(g_val, 0, 255, 0, 100)
    b_val = map_rgb(b_val, 0, 255, 0, 100)

    # Change duty cycle
    p_R.ChangeDutyCycle(r_val)
    p_G.ChangeDutyCycle(g_val)
    p_B.ChangeDutyCycle(b_val)


def destroy():
    """Reset pins
    """
    # buzzer
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    # rgb
    p_R.stop()
    p_G.stop()
    p_B.stop()
    for _, pin in RGB_PINS.items():
        # Turn off all leds
        GPIO.output(RGB_PINS[pin], GPIO.HIGH)

    GPIO.cleanup()


def loop():
    """Main loop for pi-athlon
    """
    start_time = time.time()
    while True:
        if time.time() > start_time + 5:
            start_time = time.time()
            temp = read_sensor()
            if temp > 30000:
                set_color(BLUE)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                robot.stop()
                time.sleep(10)
            else:
                set_color(GREEN)
                GPIO.output(BUZZER_PIN, GPIO.HIGH)

        right_sensor = GPIO.input(13)
        left_sensor = GPIO.input(16)

        if (right_sensor == 1) and (left_sensor == 0):
            if GPIO.input(OBSTACLE_PIN) == 0:
                set_color(RED)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                robot.stop()
            else:
                set_color(GREEN)
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                robot.right(40)

        if (left_sensor == 1) and (right_sensor == 0):
            if GPIO.input(OBSTACLE_PIN) == 0:
                set_color(RED)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                robot.stop()
            else:
                set_color(GREEN)
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                robot.left(40)

        if (right_sensor == 1) and (left_sensor == 1):
            if GPIO.input(OBSTACLE_PIN) == 0:
                set_color(RED)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                robot.stop()
            else:
                set_color(GREEN)
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                robot.forward(90)

        if (right_sensor == 0) and (left_sensor == 0):
            if GPIO.input(OBSTACLE_PIN) == 0:
                set_color(RED)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                robot.stop()
            else:
                set_color(GREEN)
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                robot.backward(40)


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
