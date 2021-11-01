import time
import RPi.GPIO as GPIO
import Robot

right_pin = 13
left_pin = 16
buzzer_pin = 15
obstacle_pin = 18
rgb_pins = {"pin_R": 35, "pin_G": 38, "pin_B": 40}
red = 0x00FFFF
green = 0xFF00FF
blue = 0xFFFF00
temp = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(right_pin, GPIO.IN)
GPIO.setup(left_pin, GPIO.IN)

LEFT_TRIM = 0
RIGHT_TRIM = 0

robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

# rgb
for pin in rgb_pins:
    # Set pins' mode is output
    GPIO.setup(rgb_pins[pin], GPIO.OUT)
    # Set pins to high(+3.3V) to off led
    GPIO.output(rgb_pins[pin], GPIO.HIGH)

# set Frequece to 2KHz
p_R = GPIO.PWM(rgb_pins['pin_R'], 2000)
p_G = GPIO.PWM(rgb_pins['pin_G'], 2000)
p_B = GPIO.PWM(rgb_pins['pin_B'], 2000)

# Initial duty Cycle = 0(leds off)
p_R.start(0)
p_G.start(0)
p_B.start(0)


def read_sensor():
    with open("/sys/bus/w1/devices/28-0314979462d3/w1_slave") as input_file:
        try:
            lines = input_file.readlines()
            temp = lines[-1].split("t=")[1].strip()
            return int(temp)
        except IndexError as e:
            print("Unable to get temp")
            print(e)
            return 0


def setup():
    # buzzer
    GPIO.setup(buzzer_pin, GPIO.OUT)
    # GPIO.output(buzzer_pin, GPIO.LOW)
    # obstacle
    GPIO.setup(obstacle_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def map_rgb(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def setColor(color_str):
    R_val = (color_str & 0xff0000) >> 16
    G_val = (color_str & 0x00ff00) >> 8
    B_val = (color_str & 0x0000ff) >> 0

    R_val = map_rgb(R_val, 0, 255, 0, 100)
    G_val = map_rgb(G_val, 0, 255, 0, 100)
    B_val = map_rgb(B_val, 0, 255, 0, 100)

    # Change duty cycle
    p_R.ChangeDutyCycle(R_val)
    p_G.ChangeDutyCycle(G_val)
    p_B.ChangeDutyCycle(B_val)


def destroy():
    # buzzer
    GPIO.output(buzzer_pin, GPIO.LOW)
    # rgb
    p_R.stop()
    p_G.stop()
    p_B.stop()
    for pin in rgb_pins:
        # Turn off all leds
        GPIO.output(rgb_pins[pin], GPIO.HIGH)

    GPIO.cleanup()


def loop():
    start_time = time.time()
    while True:
        if time.time() > start_time + 5:
            start_time = time.time()
            temp = read_sensor()
            if temp > 30000:
                setColor(blue)
                GPIO.output(buzzer_pin, GPIO.LOW)
                robot.stop()
                time.sleep(10)
            else:
                setColor(green)
                GPIO.output(buzzer_pin, GPIO.HIGH)

        RIGHT_SENSOR = GPIO.input(13)
        LEFT_SENSOR = GPIO.input(16)

        if (RIGHT_SENSOR == 1) and (LEFT_SENSOR == 0):
            if GPIO.input(obstacle_pin) == 0:
                setColor(red)
                GPIO.output(buzzer_pin, GPIO.LOW)
                robot.stop()
            else:
                setColor(green)
                GPIO.output(buzzer_pin, GPIO.HIGH)
                robot.right(40)

        if (LEFT_SENSOR == 1) and (RIGHT_SENSOR == 0):
            if GPIO.input(obstacle_pin) == 0:
                setColor(red)
                GPIO.output(buzzer_pin, GPIO.LOW)
                robot.stop()
            else:
                setColor(green)
                GPIO.output(buzzer_pin, GPIO.HIGH)
                robot.left(40)

        if (RIGHT_SENSOR == 1) and (LEFT_SENSOR == 1):
            if GPIO.input(obstacle_pin) == 0:
                setColor(red)
                GPIO.output(buzzer_pin, GPIO.LOW)
                robot.stop()
            else:
                setColor(green)
                GPIO.output(buzzer_pin, GPIO.HIGH)
                robot.forward(90)

        if (RIGHT_SENSOR == 0) and (LEFT_SENSOR == 0):
            if GPIO.input(obstacle_pin) == 0:
                setColor(red)
                GPIO.output(buzzer_pin, GPIO.LOW)
                robot.stop()
            else:
                setColor(green)
                GPIO.output(buzzer_pin, GPIO.HIGH)
                robot.backward(40)


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
