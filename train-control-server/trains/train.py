#!/usr/bin/env python3
from __future__ import print_function, division

from http.server import BaseHTTPRequestHandler

from gpiozero import Motor, PWMLED
import json
import os.path

# hacky
ON_PI = os.path.isfile("/sys/firmware/devicetree/base/model")


# motor = Motor(23,24)

class Train():

    @staticmethod
    def getDefaultConfig():
        return {
            "motorPin0": 23,
            "motorPin1": 24,
            "real": ON_PI,
            "deadZone": 0.05,
            "frontWhitePin": None,
            "frontRedPin": None,
            "rearRedPin": None,
            "rearWhitePin": None,
            "whiteBrightness": 1,
            "redBrightness": 1
        }

    def __init__(self, config):
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
        self.frontRedLight = None
        self.rearWhiteLight = None
        self.rearRedLight = None
        self.redBrightness = config["redBrightness"]
        self.whiteBrightness = config["whiteBrightness"]
        # really on a pi with a motor?
        self.real = config["real"]
        self.deadZone = config["deadZone"]
        # user-facing controls
        self.requestedSpeed = 0
        self.headlights = False
        self.reverse = False

        if config["real"]:
            self.motor = Motor(config["motorPin0"], config["motorPin1"])
            if config["frontWhitePin"] is not None:
                self.frontWhiteLight = PWMLED(config["frontWhitePin"])
            if config["frontRedPin"] is not None:
                self.frontRedLight = PWMLED(config["frontRedPin"])
            if config["rearWhitePin"] is not None:
                self.rearWhiteLight = PWMLED(config["rearWhitePin"])
            if config["rearRedPin"] is not None:
                self.rearRedLight = PWMLED(config["rearRedPin"])

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

    def hasHeadlights(self):
        '''
        return true if this train is configured with any headlights
        '''
        return self.frontWhiteLight is not None or self.rearWhiteLight is not None \
               or self.frontRedLight is not None or self.rearRedLight is not None

    def setHeadlights(self, headlights):
        self.headlights = headlights

        frontWhite = {}
        frontRed = {}
        rearWhite = {}
        rearRed = {}

        lights = [frontWhite, frontRed, rearWhite, rearRed]

        frontWhite['on'] = False
        frontRed['on'] = False
        rearWhite['on'] = False
        rearRed['on'] = False
        frontWhite['led'] = self.frontWhiteLight
        frontRed['led'] = self.frontRedLight
        rearWhite['led'] = self.rearWhiteLight
        rearRed['led'] = self.rearRedLight
        frontWhite['brightness'] = self.whiteBrightness
        frontRed['brightness'] = self.redBrightness
        rearWhite['brightness'] = self.whiteBrightness
        rearRed['brightness'] = self.redBrightness

        if self.headlights:
            if self.reverse:
                frontRed['on'] = True
                rearWhite['on'] = True
            else:
                frontWhite['on'] = True
                rearRed['on'] = True

        for light in lights:
            if light['led'] is not None:
                if light['on']:
                    light['led'].value = light['brightness']
                else:
                    light['led'].off()

    def setReverse(self, reverse):
        self.reverse = reverse
        currentSpeed = self.getSpeed()
        if currentSpeed < 0 != reverse and currentSpeed != 0:
            # need to change current speed, since we're going in the wrong direction
            self.setSpeed(-currentSpeed)
        # force the headlights to sort themselves out
        self.setHeadlights(self.headlights)

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
        return json.dumps(self.getSimpleObject())

    def getSimpleObject(self):
        return {"speed": abs(self.getSpeed()), "deadZone": self.deadZone, "reverse": self.reverse,
                           "headlights": self.headlights, "hasHeadlights": self.hasHeadlights()}


class TrainServerHTTPHandler(BaseHTTPRequestHandler):

    train = None

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        print("GET - reporting status")
        self.returnSerialised()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print(body.decode("ASCII"))

        data = json.loads(body.decode("ASCII"))

        speed = abs(TrainServerHTTPHandler.train.getSpeed())
        reverse = TrainServerHTTPHandler.train.getReverse()

        if 'speed' in data:
            speed = float(data['speed'])
            print("Speed: " + str(speed))
        if 'reverse' in data:
            reverse = bool(data['reverse'])
            print("Reverse: " + ("True" if reverse else "False"))
            TrainServerHTTPHandler.train.setReverse(reverse)
        if 'headlights' in data:
            headlights = bool(data['headlights'])
            TrainServerHTTPHandler.train.setHeadlights(headlights)
            print("Headlights: " + ("True" if headlights else "False"))

        TrainServerHTTPHandler.train.setSpeed(speed * (-1 if reverse else 1))

        self.send_response(200)
        self.end_headers()
        self.returnSerialised()

    def returnSerialised(self):
        summary = {"type": "train", "train": TrainServerHTTPHandler.train.getSimpleObject()}
        self.wfile.write(json.dumps(summary).encode("ASCII"))