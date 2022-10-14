"""Project 4 pi-athlon

This project is intended to have the pi-athlon use a UI to move

"""
import RPi.GPIO as GPIO
import Robot
# flask
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

# init pins
BUZZER_PIN = 15
RGB_PINS = {"pin_R": 35, "pin_G": 38, "pin_B": 40}
RED = 0x00FFFF
GREEN = 0xFF00FF
BLUE = 0xFFFF00

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

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


def setup():
    """Setup buzzer pins"""
    # buzzer
    GPIO.setup(BUZZER_PIN, GPIO.OUT)


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


def play_buzzer(time_in_secs):
    """Plays Buzzer"""
    # todo
    pass


def move_robot(direction, time_in_secs=2, speed=50):
    """Moves Robot"""
    # toto
    pass


# init flask
app = Flask(__name__)
# init sensors
setup()


@app.route("/")
def home():
    """Returns Home"""
    return render_template("index.html")


@app.route("/led/<color>")
def app_set_color(color):
    """Sets Color"""
    print("color", color)
    # set the LED of the robot for specified color
    if color == "red":
        set_color(RED)
    if color == "green":
        set_color(GREEN)
    if color == "blue":
        set_color(BLUE)

    # return message to client
    return jsonify({"led": color})


@app.route("/direction/<direction>")
def app_move_robot(direction):
    """Moves robot"""
    speed = int(request.args.get("speed"))
    duration = int(request.args.get("duration"))
    print("speed", speed)
    print("duration", duration)
    # move the robot with the specified direction, speed and duration
    move_robot(direction, duration, speed)

    # return message to client
    return jsonify({
        "direction": direction,
        "speed": speed,
        "duration": duration
    })


@app.route("/buzzer")
def app_play_buzzer():
    """Plays Buzzer"""
    print("buzzer")
    # activate the robot buzzer
    play_buzzer(5)

    # return message to client
    return jsonify({
        "buzzer": "buzzer"
    })
