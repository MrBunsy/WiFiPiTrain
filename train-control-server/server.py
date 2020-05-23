#!/usr/bin/env python3
from __future__ import print_function, division
from http.server import HTTPServer

from trains.point import PointsServer, PointsServerHTTPHandler
from trains.train import Train, TrainServerHTTPHandler
from trains.config import PiConfig

config = PiConfig()

httpd = None

if config.hasPowerLight():
    print("Configured with power light")
    light = config.getPowerLight()
    light.set(True)

if config.hasPoints():
    print("Configured with points")
    points = PointsServer(config.getPoints(), config.getSimultaneousPoints())
    PointsServerHTTPHandler.points = points
    httpd = HTTPServer(('0.0.0.0', 8000), PointsServerHTTPHandler)
elif config.isTrain():
    print("Configured as train")
    train = Train(config.getTrain())
    TrainServerHTTPHandler.train = train
    httpd = HTTPServer(('0.0.0.0', 8000), TrainServerHTTPHandler)
else:
    print("Server not configured to do anything, exiting. Try adding /etc/trains.json")
    exit()



httpd.serve_forever()

