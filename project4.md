Overview
In the last project you learned how to control your robot by downloading a file, parsing it for instructions and having the robot perform those instructions. Now you will gain full control of your robot by creating an API out of the commands the robot can perform and then use a client (in this case a web based controller simulator) to control it.

What exactly is an API? You might have heard of this before, API is an Application Programing Interface. Traditional applications, the API is what’s between the client and server that takes HTTP rest commands from the client, sends to the server, the server executes some code and returns the response to client.


We’ll be creating an API for the Robot in this project:


The API will take instructions for directions (forward, backward, right, left), led (red, green, blue), buzzer, speed and duration from a web based controller simulator and translate them into the robot functions we did in the previous projects. After the project you will have full control of your robot!

We will be using the Flask library to create the API. Flask will turn the Robot into a web server and we will create routes (API End points) that will map to a robot function. For example:


http://[raspberry-pi-ip-address]/red
when you go to this url, it will turn the robot LED red

Similarly you can create:


http://[raspberry-pi-ip-address]/blue
http://[raspberry-pi-ip-address]/green
Each of those will turn the robot LED their respective colors.

Since these functions perform similar actions (changing the color of the LED), we can group them together as a resource, called led, with the color being dynamic. So would be:


http://[raspberry-pi-ip-address]/led/red
http://[raspberry-pi-ip-address]/led/green
http://[raspberry-pi-ip-address]/led/blue
This technique is creating a REST API resource as a URI (Uniform Resource Identified) with led being the resource and the color as the identifier. The Flask example of this can be found here. An example for the robot could be:


@app.route('/led/<color>')
def app_set_color(color):
    # set the color the LED for the robot
    return f"Set color {color}!"
 

Additionally, you can use query parameters to pass arguments to an API endpoint. For example, let’s say we have created an API endpoint for all the moves of the robot as:


http://[raspberry-pi-ip-address]/direction/forward
http://[raspberry-pi-ip-address]/direction/backward
http://[raspberry-pi-ip-address]/direction/right
http://[raspberry-pi-ip-address]/direction/left
And if we want to control how fast the robot moves for each direction and for how long, we can pass those values as query parameters. In this case to move the robot forward at speed 100 for 2 seconds we would go to


http://[raspberry-pi-ip-address]/direction/forward?speed=100&duration=2
To do this in Flask we can access the query parameter using the request library


from flask import request

@app.route("/direction/<direction>")
def app_move_robot(direction):
    speed = int(request.args.get("speed"))
    duration = int(request.args.get("duration"))
    move_robot(direction, duration, speed)
    return f"Moving robot {direction} at {speed} for {duration}!"
