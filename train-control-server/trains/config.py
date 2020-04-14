from .point import Point
from .train import Train
import json


class PiConfig:
    '''
    A class to process configuration loaded from disk
    '''

    def  __init__(self, path="/etc/trains.json"):
        self.configBlob = {}
        with open(path, "r") as configFile:
            self.configBlob = json.load(configFile)

    def hasPoints(self):
        '''
        this pi controls at least one point
        :return:
        '''
        if "points" in self.configBlob:
            return len(self.configBlob["points"]) > 0

    def getSimultaniousPoints(self):
        if "simultaniousPoints" in self.configBlob:
            return int(self.configBlob["simultaniousPoints"])
        else:
            return 1

    def getPoints(self):
        '''
        Get array of points from the config file
        :return: array of point config dicts
        '''
        points = []
        if self.hasPoints():
            for json in self.configBlob["points"]:
                config = Point.getDefaultConfig()
                if "pwmPin" in json:
                    config["pwmPin"] = int(json["pwmPin"])
                if "servoPowerPin" in json:
                    config["serverPowerPin"] = int(json["servoPowerPin"])
                if "position0PWM" in json:
                    config["position0PWM"] = float(json["position0PWM"])
                if "position1PWM" in json:
                    config["position1PWM"] = float(json["position1PWM"])
                if "startPosition" in json:
                    config["startPosition"] = int(json["startPosition"])
                if "timeToChange" in json:
                    config["timeToChange"] = float(json["timeToChange"])
                points.append(config)

        return points

    def isTrain(self):
        '''
        This pi is driving a single train
        :return:
        '''
        return "train" in self.configBlob

    def getTrain(self):
        if not self.isTrain():
            return None
        json = self.configBlob["train"]
        config = Train.getDefaultConfig()
        if "motorPin0" in json:
            config["motorPin0"] = int(json["motorPin0"])
        if "motorPin1" in json:
            config["motorPin1"] = int(json["motorPin1"])
        if "deadZone" in json:
            config["deadZone"] = float(json["deadZone"])
        if "frontWhitePin" in json:
            config["frontWhitePin"] = int(json["frontWhitePin"])
        if "rearWhitePin" in json:
            config["rearWhitePin"] = int(json["rearWhitePin"])
        if "frontRedPin" in json:
            config["frontRedPin"] = int(json["frontRedPin"])
        if "rearRedPin" in json:
            config["rearRedPin"] = int(json["rearRedPin"])
        if "whiteBrightness" in json:
            config["whiteBrightness"] = float(json["whiteBrightness"])
        if "redBrightness" in json:
            config["redBrightness"] = float(json["redBrightness"])

        return config