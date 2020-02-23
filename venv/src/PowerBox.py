#!/usr/bin/python3

import PowerBoxConfig
import RPi.GPIO as GPIO
from flask import Flask, jsonify, request

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
pinList = [4, 17, 27, 22, 5, 6, 13, 19]
channelStatus = ['ON', 'ON', 'ON', 'ON', 'ON', 'ON', 'ON', 'ON']
CHANNEL_ON = GPIO.LOW
CHANNEL_OFF = GPIO.HIGH

class PowerBox:
    def __init__(self):
        self.cfg = PowerBoxConfig.PowerBoxConfig()

    def initialize(self):
        for i in pinList:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)

    @app.route('/PowerBox/getChannelStatus', methods=['GET'])
    def getChannelStatus():
        return jsonify({'channelStatus': channelStatus})

    @app.route('/PowerBox/setChannelState', methods=['POST'])
    def setChannelState():
        print("setChannelState() called.")

#        if not request.json:
#            abort(400)

        channel = request.json['channel']
        state = request.json['state']
        print("channel: ", channel)
        print("state: ", state)

        channelStatus[int(channel)-1] = state

        if(state=="ON"):
            cmd = CHANNEL_ON
        elif(state=="OFF"):
            cmd = CHANNEL_OFF
        else:
            return "Invalid channel"

        GPIO.output(pinList[int(channel)-1],cmd)

        return "OK"

    def run(self):
        app.run(debug=True,host=self.cfg.getAddress(),port=int(self.cfg.getPort()))

if __name__ == '__main__':
    powerBox = PowerBox()
    powerBox.initialize()
    powerBox.run()


