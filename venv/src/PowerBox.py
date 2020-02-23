#!/usr/bin/python3

import PowerBoxConfig

try:
    import RPi.GPIO as GPIO
    rasp_env = True
except(ImportError, RuntimeError):
    rasp_env = False

from flask import Flask, jsonify, request
import json

app = Flask(__name__)

pinList = [4, 17, 27, 22, 5, 6, 13, 19]
#channelStatus = ['ON', 'ON', 'ON', 'ON', 'ON', 'ON', 'ON', 'ON']
channelStatus = {
    1:"OFF",
    2:"OFF",
    3: "OFF",
    4: "OFF",
    5: "OFF",
    6: "OFF",
    7: "OFF",
    8: "OFF",
}

class PowerBox:
    def __init__(self):
        self.cfg = PowerBoxConfig.PowerBoxConfig()

    def initialize(self):
        if(rasp_env):
            GPIO.setmode(GPIO.BCM)
            CHANNEL_ON = GPIO.LOW
            CHANNEL_OFF = GPIO.HIGH
            for i in pinList:
                GPIO.setup(i, GPIO.OUT)
                GPIO.output(i, GPIO.HIGH)
        else:
            print("Running in a test enviroment!")


    @app.route('/PowerBox/getChannelStatus', methods=['GET'])
    def getChannelStatus():
        #return jsonify({'channelStatus': channelStatus})
        return json.dumps(channelStatus)

    @app.route('/PowerBox/setChannelState', methods=['POST'])
    def setChannelState():
        print("setChannelState() called.")

        channel = request.json['channel']
        state = request.json['state']
        print("channel: ", channel)
        print("state: ", state)

        channelStatus[int(channel)] = state

        if(rasp_env):
            if(state=="ON"):
                cmd = CHANNEL_ON
            elif(state=="OFF"):
                cmd = CHANNEL_OFF
            else:
                return "Invalid channel"

            GPIO.output(pinList[int(channel)-1],cmd)

        return json.dumps(channelStatus)

    def run(self):
        app.run(debug=True,host=self.cfg.getAddress(),port=int(self.cfg.getPort()))

if __name__ == '__main__':
    powerBox = PowerBox()
    powerBox.initialize()
    powerBox.run()


