#!/usr/bin/python3

import PowerBoxConfig

try:
    # Attempt to import the GPIO module for running on Raspberry Pi.
    # If an exception is caught, then we're not running on a Raspberry Pi.
    import RPi.GPIO as GPIO
    rasp_env = True
except(ImportError, RuntimeError):
    # Set flag indicating that we are not running on a Raspberry Pi.
    rasp_env = False

# import flask and json to run/support the lightweight web server and implement the REST API.
from flask import Flask, jsonify, request
import json

# Create flask app object
app = Flask(__name__)

# pinList contains the Raspberry Pi GPIO pin numbers used for relay channels 1-8
pinList = {
    1:0,
    2:0,
    3:0,
    4:0,
    5:0,
    6:0,
    7:0,
    8:0,
    9:0,
    10:0,
    11:0,
    12:0,
    13:0,
    14:0,
    15:0,
    16:0
}

# channelStatus holds the current state of each relay channel.  Initialize all channels to "OFF".
channelStatus = {
    1:"OFF",
    2:"OFF",
    3:"OFF",
    4:"OFF",
    5:"OFF",
    6:"OFF",
    7:"OFF",
    8:"OFF",
    9: "OFF",
    10: "OFF",
    11: "OFF",
    12: "OFF",
    13: "OFF",
    14: "OFF",
    15: "OFF",
    16: "OFF",
}

# Constants for controlling the Raspberry Pi GPIO pins
if rasp_env:
    CHANNEL_ON = GPIO.LOW
    CHANNEL_OFF = GPIO.HIGH

class PowerBox:
    """
    The PowerBox class implements functionality to control an 8-channel relay controllable via a REST API.
    """
    def __init__(self):
        """
        Initializer/Constructor for the PowerBox class.

        Args:
            :param self: reference back to this object

        Returns:
            None
        """
        self.cfg = PowerBoxConfig.PowerBoxConfig()


    def initialize(self):
        """
        Initializes the 8-channel relay.

        Args:
            :param self: reference back to this object

        Returns:
            None
        """

        # Get the pin list from the config file
        configPinList = self.cfg.getPinList()
        for i in range(1, 17):
            pinList[i] = configPinList[i]

        # If running on the Raspberry Pi, initialize the GPIO pins and set all relay channels to OFF.
        if(rasp_env):
            GPIO.setmode(GPIO.BCM)
            for i in range(1, 17):
                print("Setting up pin ", i, ":", pinList[i])
                GPIO.setup(pinList[i], GPIO.OUT)
                GPIO.output(pinList[i], CHANNEL_OFF)
            print("Running on a Raspberry Pi. GPIO channels initialized")
        else:
            print("Running in a test enviroment!")


    @app.route('/PowerBox/getChannelStatus', methods=['GET'])
    def getChannelStatus():
        """
        REST API function. Return the current channel status as a JSON.

        Args:
            None. Handled through the REST request.

        Returns:
            Current state of all channels as a JSON.
        """
        return json.dumps(channelStatus)

    @app.route('/PowerBox/setChannelState', methods=['POST'])
    def setChannelState():
        """
        Rest API function. Sets the state of a single relay channel and returns the current state of all channels.

        Args:
            None. Handled through the REST request.

        Returns:
            Current state of all channels as a JSON.
        """

        # Extract the channel number from the REST request
        channel = request.json['channel']
        # Extract the desired state (On/Off) from the REST request
        state = request.json['state']
        print("setChannelState request received:")
        print("    channel: ", '"', channel, '"')
        print("    state: ", state)

        # If we're running on a Raspberry Pi, command the GPIO pin.
        if(rasp_env):
            if(state=="ON"):
                cmd = CHANNEL_ON
            elif(state=="OFF"):
                cmd = CHANNEL_OFF
            else:
                return "Invalid channel state"

            # Command the GPIO pin.
            if (channel == '*'):
                for pin in pinList:
                   GPIO.output(pinList[pin], cmd)
                   # Change the channel state in the local dictionary
                   channelStatus[pin] = state
            else:
                GPIO.output(pinList[channel],cmd)
                # Change the channel state in the local dictionary
                channelStatus[int(channel)] = state

        # Return the current state for all channels.
        return json.dumps(channelStatus)

    @app.route('/PowerBox/runBatchCommand', methods=['POST'])
    def runBatchCommand():
        """
        Rest API function. Receive a series of timestamped command and run as a batch.

        Args:
            None. Handled through the REST request.

        Returns:
            None.
        """

        print("runBatchCommand request received.")
        return json.dumps(channelStatus)

    def run(self):
        """
        Runs the flask webserver

        Args:
            :param self: reference back to this object

        Returns:
            None
        """

        print("Starting Flask server on ",self.cfg.getAddress(), ":", self.cfg.getPort())

        # Run the flask webservice using the address and port defined in the config file.
        app.run(debug=True,host=self.cfg.getAddress(),port=int(self.cfg.getPort()))

if __name__ == '__main__':
    powerBox = PowerBox()
    powerBox.initialize()
    powerBox.run()


