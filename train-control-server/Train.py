#!/usr/bin/env python3
from __future__ import print_function, division

from gpiozero import Motor, PWMLED
import json
import os.path

# hacky
ON_PI = os.path.isfile("/sys/firmware/devicetree/base/model")


# motor = Motor(23,24)

class Train():
    def __init__(self, motorPin0=23,
                 motorPin1=24,
                 real=ON_PI,
                 deadZone=0.05,
                 frontWhite=None,
                 frontRed=None,
                 rearRed=None,
                 rearWhite=None,
                 whiteBrightness=1,
                 redBrightness=1):
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
        self.redBrightness = redBrightness
        self.whiteBrightness = whiteBrightness
        # really on a pi with a motor?
        self.real = real
        self.deadZone = deadZone
        # user-facing controls
        self.requestedSpeed = 0
        self.headlights = False
        self.reverse = False

        if real:
            self.motor = Motor(motorPin0, motorPin1)
            if frontWhite is not None:
                self.frontWhiteLight = PWMLED(frontWhite)
            if frontRed is not None:
                self.frontRedLight = PWMLED(frontRed)
            if rearWhite is not None:
                self.rearWhiteLight = PWMLED(rearWhite)
            if rearRed is not None:
                self.rearRedLight = PWMLED(rearRed)

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
        return json.dumps({"speed": abs(self.getSpeed()), "deadZone": self.deadZone, "reverse": self.reverse,
                           "headlights": self.headlights})