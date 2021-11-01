Overview
In this project you will build upon the robot created in the first and second project by downloading files containing instructions from a server onto the robot. The robot will then parse the file and act upon the instructions given. No hardware installation is needed for this project.

We will provide example instructions for you to test with. The instruction file contains "actions" and the "length of time" for which the robot should perform the action. The robot should parse the instructions and then act based on those inputs.

On the final day, you will be provided a method (FTP, SSH, or HTTP) and a file path (e.g. /instruction/robot1), userid, password, and file name along with an IP address. Your robot should use this information to get the necessary instructions and begin acting upon them. We will have three methods to download the file: FTP, HTTP, and SSH. The robot should be capable of each one these methods to download the instruction file. On the final day, your team might be given any one of these methods.

Once we download the file your robot will need to parse the file so the robot will know what actions to take (example below).  Examples of actions include LED changes, noise, or movement.

Once file download has completed:

The LED must turn GREEN and the BEEPER must turn on and off quickly for 5 seconds to notify that the actions are to begin. 

When following the instructions, if you come upon an unknown action, the Robot will turn on the Red LED and beep for 5 seconds, then continue to the next instruction. 

Extra Credit
You will be provided access to a syslog server (10.37.212.2:514). You should stream your logs to this syslog server when your script is executing.  The robot can send information about the actions it is performing such as downloading a file, moving forward, corrupted files, etc. These log messages will be displayed on a television and will help us as humans to identify what your robot is doing. Hint: Use the logging module from the python standard library. Note: When logging to syslog server please use unique identifiers that show it is your robot.

To finish, you are free to have your robot perform any function you want. Be creative have fun with it!

Below are sample libraries that you can use to complete the project, but feel free to explore other ways to complete it.

FTP - ftplib

HTTP - urllib or requests

SSH - paramiko

(When done, you can check that your robot is logging to syslog properly by logging in as the “pi” user via SSH to the server and then looking at the file contents of /var/log/rpis)

Example Instructions
Below is an example of the instructions you can expect to download. They are in JSON format. You can use the JSON contents below for your testing. (Note: all robot speeds for your file need to be set at 100 so set them to 100)


[
  {
    "action": "led_green",
    "time": 1
  },
  {
    "action": "forward",
    "time": 5
  },
  {
    "action": "led_red",
    "time": 1
  },
  {
    "action": "stop",
    "time": 1
  },
  {
    "action": "led_green",
    "time": 1
  },
  {
    "action": "backward",
    "time": 5
  },
  {
    "action": "led_red",
    "time": 1
  },
  {
    "action": "left",
    "time": 5
  },
  {
    "action": "led_blue",
    "time": 1
  },
  {
    "action": "right",
    "time": 5
  },
  {
    "action": "led_red",
    "time": 1
  },
  {
    "action": "play_sound",
    "time": 5
  }
]
The list of possible actions is listed below. Your robot should be able to perform each of these. Note: that your robot should be able to handle any unknown actions and follow the steps listed in the instructions above. Example file is located here to use for testing: 

Action

Description

forward

Robot should move forward

backward

Robot should move backward

left

Robot should move left (continue left to go in a circle)

right

Robot should move right (continue righto go in a circle)

play_sound

Robot should play a sound

led_blue

The LED on the robot should turn a solid blue, then turn off after this action is completed

led_green

The LED on the robot should turn a solid green, then turn off after this action is completed

led_red

The LED on the robot should turn a solid red, then turn off after this action is completed

stop

The robot should stop activity

Initial Setup (example: A good starting point)
Below is a template you can use as a starting point for your code. Feel free to create your own script from scratch if you prefer.


# Raspberry pi Project 3
 
def download_file_from_ftp_server(uri):
    """Download a file from a FTP server and return its contents"""
    pass
 
 
def download_file_from_http_server(uri):
    """Download a file from a HTTP web server and return its contents"""
    pass
 
 
def download_file_using_ssh(uri):
    """Download a file from a a device using SSH and return its contents"""
    pass
 
 
def follow_instructions(file_contents):
    """Parse file contents and make the robot follow instructions"""
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
    uri = "ftp://10.37.212.2/example_instructions.json"
    file_contents = download_file(uri)
    follow_instructions(file_contents)
 
if __name__ == "__main__":
    main()

Endpoint
Server that will host the instruction file and other necessary components. There you can test downloading the file from the host Pi via FTP, HTTP, and SSH.

To access the server via the internal network see information below:

PLEASE DO NOT REMOVE FILE OR MODIFY THE FILE LOCATED ON SERVER.

IP: 10.37.212.2

Method

Directory

Credentials

Method

Directory

Credentials

FTP

/var/ftp/pub OR /home/pi

User: pi | Password: V0c3r@123

SSH

/var/ssh

User: pi | Password: V0c3r@123

HTTP

/var/www/html OR http://10.37.212.2:80

None

 

SysLog
The syslog file location is: /var/log/rpis

To view the contents of the syslog file, you can ssh into 10.37.212.2 as pi user and run the command:


tail -f /var/log/rpis
This will give you a live tail view of the log and when your robot sends events to it, you can view them in real time. The “byron-ip” in the example is the custom name I gave the to the getLogger method so I can distinguish my logs from others. Note - there are some differences between python 2 syslog and python 3 syslog, so make sure you check the docs for the proper version of python you are using.

