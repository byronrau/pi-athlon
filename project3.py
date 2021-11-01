import ftplib
import requests
import paramiko
import os
from logger import pi_logger
import json
# robot
import RPi.GPIO as GPIO
import Robot
import time
# init pins
buzzer_pin = 15
obstacle_pin = 18
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
    # obstacle
    GPIO.setup(obstacle_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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


def download_file_from_ftp_server(uri):
    """Download a file from a FTP server and return its contents"""

    pi_logger.debug("Download file from FTP")
    ftp = ftplib.FTP("10.37.212.2")
    ftp.login("pi", "V0c3r@123")
    ftp.cwd("/var/ftp/pub")
    with open("example_instuctions.json", "wb") as download_file:
        ftp.retrbinary(f"RETR example_instructions.json", download_file.write)
    ftp.quit()


def download_file_from_http_server(uri):
    """Download a file from a HTTP web server and return its contents"""

    pi_logger.debug("Download file from HTTP")
    r = requests.get(uri)
    with open("example_instructions.json", "wb") as download_file:
        download_file.write(r.content)


def download_file_using_ssh(uri):
    """Download a file from a a device using SSH and return its contents"""

    pi_logger.debug("Download file from SSH")
    ssh_host = "10.37.212.2"
    ssh_user = "pi"
    ssh_pw = "V0c3r@123"
    remote_dir = "/var/ssh/example_instructions.json"
    local_dir = os.path.join(os.getcwd(), "example_instructions.json")
    s = paramiko.Transport((ssh_host, 22))
    s.connect(username=ssh_user, password=ssh_pw)
    sftp = paramiko.SFTPClient.from_transport(s)
    sftp.get(remote_dir, local_dir)


def start_instructions():
    """Robot will turn LED green and beep 5 secs"""
    setColor(green)
    start_time = time.time()
    while True:
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(buzzer_pin, GPIO.LOW)
        time.sleep(0.5)
        if time.time() > start_time + 5:
            return


def follow_instruction(instruction):
    """follow single instruction dict with keys action, time """
    if instruction["action"] == "forward":
        start_time = time.time()
        while True:
            robot.foward(10)
            if time.time() > start_time + int(instruction["time"]):
                return
    if instruction["action"] == "backward":
        start_time = time.time()
        while True:
            robot.backward(10)
            if time.time() > start_time + int(instruction["time"]):
                return
    if instruction["action"] == "left":
        start_time = time.time()
        while True:
            robot.left(10)
            if time.time() > start_time + int(instruction["time"]):
                return
    if instruction["action"] == "right":
        start_time = time.time()
        while True:
            robot.right(10)
            if time.time() > start_time + int(instruction["time"]):
                return
    if instruction["action"] == "play_sound":
        start_time = time.time()
        while True:
            GPIO.output(buzzer_pin, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(buzzer_pin, GPIO.LOW)
            time.sleep(0.5)
            if time.time() > start_time + int(instruction["time"]):
                return
    if instruction["action"] == "led_blue":
        start_time = time.time()
        while True:
            setColor(blue)
            if time.time() > start_time + int(instruction["time"]):
                return
    if instruction["action"] == "led_green":
        start_time = time.time()
        while True:
            setColor(green)
            if time.time() > start_time + int(instruction["time"]):
                return
    if instruction["action"] == "led_red":
        start_time = time.time()
        while True:
            setColor(red)
            if time.time() > start_time + int(instruction["time"]):
                return
    if instruction["action"] == "stop":
        start_time = time.time()
        while True:
            robot.stop()
            if time.time() > start_time + int(instruction["time"]):
                return


def follow_instructions(file_name):
    """Parse file contents and make the robot follow instructions"""

    pi_logger.debug("Starting robot instructions")
    start_instructions()

    with open(file_name) as input_json:
        data = json.load(input_json)
        for instruction in data:
            print(
                f"[instruction]: {instruction['action']} [time]: {instruction['time']}")

    pass


def download_file(uri):
    if uri.startswith("ftp://"):
        method = download_file_from_ftp_server
    elif uri.startswith("http://"):
        method = download_file_from_http_server
    elif uri.startswith("ssh://"):
        method = download_file_using_ssh
    else:
        raise ValueError("Invalid method")
    file_contents = method(uri)
    return file_contents


def main():
    pi_logger.debug("Byron's starting Project 3")
    # setup robot
    setup()

    uri = "http://10.37.212.2/example_instructions.json"
    # uri = "ftp://10.37.212.2/example_instructions.json"
    # uri = "ssh://10.37.212.2/example_instructions.json"
    file_name = uri.split("/")[-1]
    method = uri.split(":")[0]
    pi_logger.debug(f"Method is {method} File name is {file_name}")

    if method == "http":
        download_file_from_http_server(uri)
    if method == "ftp":
        download_file_from_ftp_server(uri)
    if method == "ssh":
        download_file_using_ssh(uri)

    follow_instructions(file_name)

    destroy()


if __name__ == "__main__":
    main()
