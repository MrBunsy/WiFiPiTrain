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
from trains.point import Point
# import concurrent.futures
import threading

#TODO load config

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

class PointsServer:

    def __init__(self, max_simultaneous = 1):
        '''

        :param max_simultaneous: how active servos at once (limit max power draw)
        '''
        #TODO load from config
        self.points = [
            Point()
        ]
        self.max_simultaneous = max_simultaneous
        self.lock = threading.RLock()
        self.condition = threading.Condition()
        self.jobs = []
        self.thread = threading.Thread(target=serviceQueue, args=(self,), daemon=True)
        self.thread.start()

        #self.threadPool = concurrent.futures.ThreadPoolExecutor(max_simultaneous)



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
            #future = self.threadPool.submit(self.points[pointIndex].setPostionBlocking, self.points[pointIndex], position)
            #done = future.done()
            #print("done? {}".format("YES" if done else "NO"))
            # self.points[pointIndex].setPostionBlocking(position)
            with self.lock:
                self.jobs.append({"index":pointIndex, "position": position})
                print("job submitted")
            with self.condition:
                print("notifying")
                self.condition.notify_all()
        else:
            print("Invalid point")

points = PointsServer()



class PointsServerHTTPHandler(BaseHTTPRequestHandler):
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
            points.setPosition(point_index, position)

        self.send_response(200)
        self.end_headers()
        self.returnSerialised()


    def returnSerialised(self):
        summary = {"type": "points", "points": points.getSimpleObject()}
        self.wfile.write(json.dumps(summary).encode("ASCII"))


httpd = HTTPServer(('0.0.0.0', 8000), PointsServerHTTPHandler)
httpd.serve_forever()
