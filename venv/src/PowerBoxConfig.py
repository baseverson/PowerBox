import configparser
import sys

defaultConfigFile = "../config/PowerBox1.cfg"

class PowerBoxConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()

        if len(sys.argv) >=2:
            configFile = sys.argv[1]
        else:
            configFile = defaultConfigFile
        print("Config file: " + configFile)

        self.config.read(configFile)

#        print("Sections: ", self.config.sections())
#
#        for section in self.config.sections():
#            print(section)
#            for key in self.config[section]:
#                print("    ",key,"=",self.config[section][key])

    def getNumChannels(self):
        return self.config.get('General', 'channels')

    def getPort(self):
        return self.config.get('General', 'port')

    def getAddress(self):
        return self.config.get('General', 'address')
