#!/usr/bin/env python3
from __future__ import print_function, division

from gpiozero import Servo, DigitalOutputDevice
import json
import os.path
import time
import threading

# hacky
ON_PI = os.path.isfile("/sys/firmware/devicetree/base/model")


# motor = Motor(23,24)

class Point():
    def __init__(self, pwnPin=17,
                 servoPowerPin=21,
                 real=ON_PI,
                 position0PWM=-1.0,
                 position1PWM=1.0,
                 startPosition = 0,
                 timeToChange = 1):
        '''

        :param pwmPin the pin which connects to the PWM input of the servo
        :param servoPowerPin the pin which controls the relay for power to the servo (high=power on, low (default) = power off
        :param position0PWM duty cycle which puts servo in position 0
        :param position1PWM duty cycle which puts servo in position 1
        :param real is this on a real pi? (false only for certain testing)
        '''
        self.servo = None
        self.relay = None
        #is position actively changing?
        self.changing = True
        self.timeToChange = timeToChange
        self.lock = threading.RLock()

        #unknown at startup
        self.position = -1

        # really on a pi with a motor?
        self.real = real
        self.position0 = position0PWM
        self.position1 = position1PWM

        if real:
            self.servo = Servo(pwnPin)
            self.relay = DigitalOutputDevice(servoPowerPin)

    def getPosition(self):
        '''
        get position, 0 or 1
        :return:
        '''
        self.lock.acquire()
        position = self.position
        self.lock.release()
        return position


    def setPostionBlocking(self, position = 0):
        '''
        Will block until the point has been changed (few seconds)
        :param position:
        :return:
        '''
        print("point setting to position {}".format(position))
        self.lock.acquire()
        self.changing = True
        self.position = position
        if self.servo:
            print("setting servo")
            self.servo.value = self.position0 if self.position == 0 else self.position1
        self.lock.release()
        if self.relay:
            print("setting relay on")
            self.relay.on()
            time.sleep(self.timeToChange)
            print("setting relay off")
            self.relay.off()

        self.lock.acquire()
        self.changing = False
        self.lock.release()

    def serialise(self):
        return json.dumps(self.getSimpleObject())

    def getSimpleObject(self):
        '''
        get a simple representation, good for serialising
        :return:
        '''
        self.lock.acquire()
        simple = {"position": self.position, "changing": self.changing}
        self.lock.release()
        return simple
    '''
    
    '''