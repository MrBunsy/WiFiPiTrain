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
        # really on a pi with a motor?
        self.real = real
        self.deadZone = deadZone
        # user-facing controls
        self.requestedSpeed = 0
        self.headlights = False
        self.reverse = False
        if real:
            self.motor = Motor(motorPin0, motorPin1)
            # self.frontWhiteLight = PWMLED()
            # TODO lights

    def getSpeed(self):
        '''
        get speed, -1 to +1
        :return:
        '''
        speed = self.requestedSpeed
        # bodge, pretend we're at the deadzone speed even if we're not trying to move the motor
        if self.real and abs(self.requestedSpeed) > self.deadZone:
            return self.motor.value
        return speed

    def getReverse(self):
        return self.reverse

    def setHeadlights(self, headlights):
        self.headlights = headlights
        #TODO actually change some GPIO based on settings

    def setReverse(self, reverse):
        self.reverse = reverse
        currentSpeed = self.getSpeed()
        if currentSpeed < 0 != reverse and currentSpeed != 0:
            # need to change current speed, since we're going in the wrong direction
            self.setSpeed(-currentSpeed)

    def setSpeed(self, speed):
        '''

        :param speed: between -1 and 1, 0 represents not moving
        :return:
        '''
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
        return json.dumps({"speed": self.getSpeed(), "deadZone": self.deadZone, "reverse": self.reverse,
                           "headlights": self.headlights})


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

        data = json.loads(body.decode("ASCII"))

        speed = abs(train.getSpeed())
        reverse = train.getReverse()

        if 'speed' in data:
            speed = float(data['speed'])
        if 'reverse' in data:
            reverse = bool(data['reverse'])
            train.setReverse(reverse)
        if 'headlights' in data:
            train.setHeadlights(bool(data['headlights']))

        train.setSpeed(speed * (-1 if reverse else 1))


        self.send_response(200)
        self.end_headers()
        self.wfile.write(train.serialise().encode("ASCII"))


httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
