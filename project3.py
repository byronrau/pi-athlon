"""Project 2 pi-athlon

This project is intended to have the pi-athlon follow a line and self drive
itself along a track. Also adds temperate sensor reading and buzzer for
object detection.

"""
import os
import json
import time
import ftplib
import requests
import paramiko
from logger import pi_logger
# robot
import RPi.GPIO as GPIO
import Robot
# init pins
BUZZER_PIN = 15
OBSTACLE_PIN = 18
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
    """Setup buzzer pins
    """
    # buzzer
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    # obstacle
    GPIO.setup(OBSTACLE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def map_rgb(x_val, in_min, in_max, out_min, out_max):
    """Sets the RGB values for light

    Args:
        x_val (int): x value
        in_min (int): input min
        in_max (int): input max
        out_min (int): output min
        out_max (int): output max
    """
    return (x_val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def set_color(col):
    """Sets color

    Args:
        color_str (str): name of color
    """
    r_val = (col & 0xff0000) >> 16
    g_val = (col & 0x00ff00) >> 8
    b_val = (col & 0x0000ff) >> 0

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


def download_file_from_ftp_server():
    """Download a file from a FTP server and return its contents"""

    pi_logger.debug("Download file from FTP")
    ftp = ftplib.FTP("10.37.212.2")
    ftp.login("pi", "V0c3r@123")
    ftp.cwd("/var/ftp/pub")
    with open("example_instuctions.json", "wb") as downloaded_file:
        ftp.retrbinary(f"RETR example_instructions.json", downloaded_file.write)
    ftp.quit()


def download_file_from_http_server(uri):
    """Download a file from a HTTP web server and return its contents"""

    pi_logger.debug("Download file from HTTP")
    res = requests.get(uri)
    with open("example_instructions.json", "wb") as downloaded_file:
        downloaded_file.write(res.content)


def download_file_using_ssh():
    """Download a file from a a device using SSH and return its contents"""

    pi_logger.debug("Download file from SSH")
    ssh_host = "10.37.212.2"
    ssh_user = "pi"
    ssh_pw = "V0c3r@123"
    remote_dir = "/var/ssh/example_instructions.json"
    local_dir = os.path.join(os.getcwd(), "example_instructions.json")
    s_con = paramiko.Transport((ssh_host, 22))
    s_con.connect(username=ssh_user, password=ssh_pw)
    sftp = paramiko.SFTPClient.from_transport(s_con)
    sftp.get(remote_dir, local_dir)


def start_instructions():
    """Robot will turn LED green and beep 5 secs"""
    set_color(GREEN)
    start_time = time.time()
    while True:
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
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
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(0.5)
            if time.time() > start_time + int(instruction["time"]):
                return
    if instruction["action"] == "led_blue":
        start_time = time.time()
        while True:
            set_color(BLUE)
            if time.time() > start_time + int(instruction["time"]):
                return
    if instruction["action"] == "led_green":
        start_time = time.time()
        while True:
            set_color(GREEN)
            if time.time() > start_time + int(instruction["time"]):
                return
    if instruction["action"] == "led_red":
        start_time = time.time()
        while True:
            set_color(RED)
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

    with open(file_name, encoding="utf-8") as input_json:
        data = json.load(input_json)
        for instruction in data:
            print(
                f"[instruction]: {instruction['action']} [time]: {instruction['time']}")


def download_file(uri):
    """Downloads file"""
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
    """Main function"""
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
        download_file_from_ftp_server()
    if method == "ssh":
        download_file_using_ssh()

    follow_instructions(file_name)

    destroy()


if __name__ == "__main__":
    main()
