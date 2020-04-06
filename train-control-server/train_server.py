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
from .Train import Train


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
            print("Speed: " + str(speed))
        if 'reverse' in data:
            reverse = bool(data['reverse'])
            print("Reverse: " + ("True" if reverse else "False"))
            train.setReverse(reverse)
        if 'headlights' in data:
            headlights = bool(data['headlights'])
            train.setHeadlights(headlights)
            print("Headlights: " + ("True" if headlights else "False"))

        train.setSpeed(speed * (-1 if reverse else 1))

        self.send_response(200)
        self.end_headers()
        self.wfile.write(train.serialise().encode("ASCII"))


httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
