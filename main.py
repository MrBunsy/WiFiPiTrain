#!/usr/bin/env python3
from __future__ import print_function, division

from gpiozero import Motor, PWMLED
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
# from urllib.parse import urlparse
import urllib
from urllib.parse import parse_qs
import json

ON_PI = False


# motor = Motor(23,24)

class Train():
    def __init__(self, motorPin0=23, motorPin1=24, real=ON_PI, frontWhite=25, frontRed=8, rearRed=7, readWhite=1):
        self.motor = None;
        self.frontWhiteLight = None
        self.frontRedLights = None
        self.rearWhiteLights = None
        self.rearRedLights = None
        self.real = real
        if real:
            self.motor = Motor(motorPin0, motorPin1)
            # self.frontWhiteLight = PWMLED()
            # TODO lights

    def getSpeed(self):
        if self.real:
            return self.motor.value
        return 0


    def setSpeed(self, speed):
        '''

        :param speed: between -1 and 1, 0 represents not moving
        :return:
        '''

        if 1 < speed < -1:
            print("Invalid speed")
            return

        if self.real:
            if speed > 0:
                self.motor.forward(speed)
            elif speed < 0:
                self.motor.backward(speed)
            else:
                self.motor.stop()

    def serialise(self):
        return json.dumps({"speed": self.getSpeed()})


train = Train()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        print("GET - reporting status")
        self.wfile.write(train.serialise().encode("ASCII"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        data = parse_qs(body);

        print(data)

        if "speed" in data:
            if len(data["speed"]) > 0:
                train.setSpeed(float(data["speed"]))

        self.send_response(200)
        self.end_headers()
        # response = BytesIO()
        # response.write(b'This is POST request to  ')
        # response.write(self.path.encode('ASCII'))
        # response.write(b' Received: ')
        # response.write(body)
        # self.wfile.write(response.getvalue())
        self.wfile.write(train.serialise().encode("ASCII"))


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()


"""
POST /drive HTTP/1.1
Host: foo.example
Content-Type: application/x-www-form-urlencoded
Content-Length: 9

speed=0.6

"""