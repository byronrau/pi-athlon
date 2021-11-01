import time
# robot
import RPi.GPIO as GPIO
import Robot
# flask
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

# init pins
buzzer_pin = 15
rgb_pins = {"pin_R": 35, "pin_G": 38, "pin_B": 40}
red = 0x00FFFF
green = 0xFF00FF
blue = 0xFFFF00

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

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


def setup():
    # buzzer
    GPIO.setup(buzzer_pin, GPIO.OUT)


def map_rgb(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def set_color(color_str):
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


def play_buzzer(time_in_secs):
    # todo
    pass


def move_robot(direction, time_in_secs=2, speed=50):
    # toto
    pass


# init flask
app = Flask(__name__)
# init sensors
setup()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/led/<color>")
def app_set_color(color):
    print("color", color)
    # set the LED of the robot for specified color
    if color == "red":
        set_color(red)
    if color == "green":
        set_color(green)
    if color == "blue":
        set_color(blue)

    # return message to client
    return jsonify({"led": color})


@app.route("/direction/<direction>")
def app_move_robot(direction):
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
    print("buzzer")
    # activate the robot buzzer
    play_buzzer(5)

    # return message to client
    return jsonify({
        "buzzer": "buzzer"
    })
