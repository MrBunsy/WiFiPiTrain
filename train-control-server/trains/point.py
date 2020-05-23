#!/usr/bin/env python3
from __future__ import print_function, division

from gpiozero import Servo, DigitalOutputDevice
import json
import os.path
import time
import threading
from http.server import BaseHTTPRequestHandler

# hacky
ON_PI = os.path.isfile("/sys/firmware/devicetree/base/model")

class PowerLight():
    @staticmethod
    def getDefaultConfig():
        return {"pin":7,
                "real": ON_PI}

    def __init__(self, config):
        if config["real"]:
            self.led = DigitalOutputDevice(config["pin"])

    def set(self, on = True):
        if self.led:
            if on:
                self.led.on()
            else:
                self.led.off()

# motor = Motor(23,24)

class Point():
    @staticmethod
    def getDefaultConfig():
        return {"servoPin": 17,
                "relayPin": 21,
                "real": ON_PI,
                "position0PWM": -1.0,
                "position1PWM": 1.0,
                "startPosition": 0,
                "timeToChange": 0.5
                }

    def __init__(self, config):
        '''

        :param pwmPin the pin which connects to the PWM input of the servo
        :param servoPowerPin the pin which controls the relay for power to the servo (high=power on, low (default) = power off
        :param position0PWM duty cycle which puts servo in position 0
        :param position1PWM duty cycle which puts servo in position 1
        :param real is this on a real pi? (false only for certain testing)
        '''
        self.servo = None
        self.relay = None
        # is position actively changing?
        self.changing = True
        self.timeToChange = config["timeToChange"]
        self.lock = threading.RLock()

        # unknown at startup
        self.position = -1

        # really on a pi with a motor?
        self.real = config["real"]
        self.position0 = config["position0PWM"]
        self.position1 = config["position1PWM"]

        if config["real"]:
            self.servo = Servo(config["servoPin"])
            self.relay = DigitalOutputDevice(config["relayPin"])

    def getPosition(self):
        '''
        get position, 0 or 1
        :return:
        '''
        self.lock.acquire()
        position = self.position
        self.lock.release()
        return position

    def setPostionBlocking(self, position=0):
        '''
        Will block until the point has been changed (few seconds)
        :param position:
        :return:
        '''
        if self.position == position:
            print("already in this position, not doing anything")
            return
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


class PointsServer:

    @staticmethod
    def serviceQueue(self):
        '''
        Run forever in a thread, processing jobs that end up on the queue
        :return:
        '''

        while True:
            with self.condition:
                print("job thread waiting")
                self.condition.wait()
                print("job thread woken")
                with self.lock:
                    job = self.jobs.pop()
                    self.points[job["index"]].setPostionBlocking(job["position"])

    def __init__(self, pointsConfig, max_simultaneous=1, powerLightConfig = None):
        '''
        :param points points list loaded from configuration
        :param max_simultaneous: how active servos at once (limit max power draw)
        '''

        if powerLightConfig is not None:
            self.light = PowerLight(powerLightConfig)
            self.light.set(true)
            
        self.points = [Point(point) for point in pointsConfig]
        self.max_simultaneous = max_simultaneous
        self.lock = threading.RLock()
        self.condition = threading.Condition()
        self.jobs = []
        self.thread = threading.Thread(target=PointsServer.serviceQueue, args=(self,), daemon=True)
        self.thread.start()

    def getSimpleObject(self):
        return [point.getSimpleObject() for point in self.points]

    def setPosition(self, pointIndex, position):
        '''

        :param pointIndex:
        :param position:
        :return:
        '''

        if pointIndex < len(self.points):
            print("Submitting job to threadpool")
            # future = self.threadPool.submit(self.points[pointIndex].setPostionBlocking, self.points[pointIndex], position)
            # done = future.done()
            # print("done? {}".format("YES" if done else "NO"))
            # self.points[pointIndex].setPostionBlocking(position)
            with self.lock:
                self.jobs.append({"index": pointIndex, "position": position})
                print("job submitted")
            with self.condition:
                print("notifying")
                self.condition.notify_all()
        else:
            print("Invalid point")


class PointsServerHTTPHandler(BaseHTTPRequestHandler):

    points = None

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

        point_index = None
        position = None

        if 'point_index' in data:
            point_index = int(data['point_index'])
            print("Point: " + str(point_index))
        if 'position' in data:
            position = int(data['position'])
            print("Position: " + str(position))

        if point_index is not None and position is not None:
            '''
            Set the point, should trigger event to occur in a different thread
            '''
            print("input valid, attempting to set point {} to {}".format(point_index, position) )
            PointsServerHTTPHandler.points.setPosition(point_index, position)

        self.send_response(200)
        self.end_headers()
        self.returnSerialised()


    def returnSerialised(self):
        summary = {"type": "points", "points": PointsServerHTTPHandler.points.getSimpleObject()}
        self.wfile.write(json.dumps(summary).encode("ASCII"))
