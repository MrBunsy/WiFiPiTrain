#!/usr/bin/env python3
from __future__ import print_function, division

from gpiozero import Motor, PWMLED
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
# from urllib.parse import urlparse
import urllib
from urllib.parse import parse_qs
import json
import os.path

# hacky
ON_PI = os.path.isfile("/sys/firmware/devicetree/base/model")


# motor = Motor(23,24)

class Train():
    def __init__(self, motorPin0=23, motorPin1=24, real=ON_PI, deadZone=0.05, frontWhite=25, frontRed=8, rearRed=7,
                 readWhite=1):
        '''

        :param motorPin0:
        :param motorPin1:
        :param real:
        :param deadZone: speeds too low to attempt to move motor
        :param frontWhite:
        :param frontRed:
        :param rearRed:
        :param readWhite:
        '''
        self.motor = None;
        self.frontWhiteLight = None
        self.frontRedLights = None
        self.rearWhiteLights = None
        self.rearRedLights = None
        self.real = real
        self.deadZone = deadZone
        self.requestedSpeed = 0
        if real:
            self.motor = Motor(motorPin0, motorPin1)
            # self.frontWhiteLight = PWMLED()
            # TODO lights

    def getSpeed(self):
        speed = self.requestedSpeed
        #bodge, pretend we're at the deadzone speed even if we're not trying to move the motor
        if self.real and abs(self.requestedSpeed) > self.deadZone:
            return self.motor.value
        return speed

    def setSpeed(self, speed):
        '''

        :param speed: between -1 and 1, 0 represents not moving
        :return:
        '''

        # if 1 < speed < -1:
        #     print("Invalid speed")
        #     # return

        if speed < -1:
            speed = -1

        if speed > 1:
            speed = 1

        if self.real:
            if speed > self.deadZone:
                self.motor.forward(speed)
            elif speed < -self.deadZone:
                self.motor.backward(-speed)
            else:
                self.motor.stop()

        self.requestedSpeed = speed

    def serialise(self):
        return json.dumps({"speed": self.getSpeed(), "deadZone": self.deadZone})


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
        print(body.decode("ASCII"))
        # print(str(body))
        # data = parse_qs(body);
        #
        # print(data)

        data = json.loads(body.decode("ASCII"))

        if 'speed' in data:
            # if len(data['speed']) > 0:
            #     print("setting speed to {}".format(data['speed'][0]))
            train.setSpeed(float(data['speed']))
            # else:
            #     print("insuficient speed data")
        else:
            print("no speed data")

        self.send_response(200)
        self.end_headers()
        # response = BytesIO()
        # response.write(b'This is POST request to  ')
        # response.write(self.path.encode('ASCII'))
        # response.write(b' Received: ')
        # response.write(body)
        # self.wfile.write(response.getvalue())
        self.wfile.write(train.serialise().encode("ASCII"))


httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()

"""
POST /drive HTTP/1.1
Host: foo.example
Content-Type: application/x-www-form-urlencoded
Content-Length: 9

speed=0.6

"""

"""
POST /drive HTTP/1.1
Host: foo.example
Content-Type: application/x-www-form-urlencoded
Content-Length: 7

speed=0

"""
