#################################################
# ACRelay Web control configuration file v0.9	#
# 						#
# Configure K8090 or Arduino Relay Boards Web	#
# remote control using REST server and Ajax,	#
# in Python 2.7.3 with Twisted framework.	#
# Applied their licenses here.			#
# 						#
#						#
# (c) 2012 Agustin Nunez, AstroCamp.es		#
# Released under GNU General Public License v3	#
# Do not use it or its derivatives for 		#
# commercial purpose.				#
#################################################

import ConfigParser

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


Config = ConfigParser.ConfigParser()
Config
Config.read("acrelay.ini")
print Config.sections()

serdev = ConfigSectionMap("Ports")['serdev']
ip  = ConfigSectionMap("Networks")['ip']
port  = ConfigSectionMap("Networks")['port']

print "SerDev: %s Ip: %s Port %s" % (serdev, ip, port)

