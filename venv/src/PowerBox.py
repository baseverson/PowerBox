#!/usr/bin/python3

import PowerBoxConfig
#import socket
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
#        self.mySocket = socket.socket()
#        self.mySocket.bind((self.cfg.getAddress(),int(self.cfg.getPort())))

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

#    def Main(self):
#
#        for i in pinList:
#            GPIO.setup(i, GPIO.OUT)
#            GPIO.output(i, GPIO.HIGH)
#            #GPIO.output(i, GPIO.LOW)
#
#        while True:
#
#            print("Waiting for connection on port " + self.cfg.getPort() + "...")
#            self.mySocket.listen(1)
#            conn, addr = self.mySocket.accept()
#            print("Connection from: " + str(addr))
#
#            while True:
#                print("Waiting for message...")
#                data = conn.recv(1024).decode()
#                if not data:
#                    break
#                print("Received from User: " + data)
#                tokens = data.split(',')
#
#                #print("Token 1: ", tokens[0])
#                #print("Token 2: ", tokens[1])
#
#                cmd = GPIO.LOW
#                #print("cmd: ", cmd, "type: ", type(cmd))
#                #print("Low: ", GPIO.LOW, "type: ", type(GPIO.LOW))
#                #print("HIGH: ", GPIO.HIGH, "type: ", type(GPIO.HIGH))
#
#                if tokens[1]=="ON":
#                    cmd = GPIO.LOW
#                elif tokens[1]=="OFF":
#                    cmd = GPIO.HIGH
#
#                if(tokens[0]=="*"):
#                    for pin in pinList:
#                        #print("Setting pin ", pin, " to ", tokens[1])
#                        GPIO.output(pin,cmd)
#                else:
#                    #print("Setting pin ", str(int(tokens[0])-1), " to ", tokens[1])
#                    GPIO.output(pinList[int(tokens[0])-1],cmd)
#
#
#                conn.send(str("ACK").encode())
#
#            #        data = input(" ? ")
#            #        conn.send(data.encode())
#
#            conn.close()
#            print("Connection closed.")
#

if __name__ == '__main__':
    powerBox = PowerBox()
    powerBox.initialize()
    powerBox.run()


