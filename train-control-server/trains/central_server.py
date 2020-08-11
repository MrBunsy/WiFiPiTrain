#!/usr/bin/env python3
from __future__ import print_function, division

class CentralServer():
    @staticmethod
    def getDefaultConfig():
        return {
            "ssdp-name": "central-trains-server"
        }

    def __init__(self, config):
