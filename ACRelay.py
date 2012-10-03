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
from twisted.web import server, resource, static
from twisted.internet import protocol, reactor, task
from twisted.internet.serialport import SerialPort
from twisted.web.static import File
import time, json

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



def chksum(cmd,msk,p1,p2):
    return (((~(0x04+cmd+msk+p1+p2))+0x01)&0xff)
def packet(cmd,msk,p1,p2):
    return str(bytearray([0x04,cmd, msk, p1, p2, chksum(cmd,msk,p1,p2), 0x0f]))
def pk2str(data):
    return " ".join(["%0.2X" % ord(c) for c in data])
def tobyte(self):
    a=0x00
    for i in range(8): a+=self[i]<<i
    return a

# Read initial parameters from "acrelay.ini" configuration file on current dir
# Different instances may simultaneos run on different directories

Config = ConfigParser.ConfigParser()
Config
Config.read("acrelay.ini")
serdev	 = ConfigSectionMap("Ports")['serdev']
baud = int(ConfigSectionMap("Ports")['baud'])
ip       = ConfigSectionMap("Networks")['ip']
port = int(ConfigSectionMap("Networks")['port'])
cycle    = ConfigSectionMap("UI")['refresh']
Relay    = [0,0,0,0,0,0,0,0]
Sensor   = [0,0,0,0,0,0,0,0]

# Callback for Serial events
class SerLog(protocol.Protocol):
    def dataReceived(self, data):
        print "<"+pk2str(data)
        d=ord(data[1])
        if (d==0x50):
            for i in range(8): Sensor[i]=(((ord(data[2]))>>i)&0x01)
        elif (d==0x51):
            for i in range(8): Relay[i]=(((ord(data[3]))>>i)&0x01)

# Handler for Home page REST event
class Root(resource.Resource):
    isLeaf=False
    def render_GET(self, request):
        request.setHeader("content-type", "text/html")
        return "Arcanoid!"
    def getChild(self, name, request):
        if name == "":
            return self
        return resource.Resource.getChild(self, name, request)

# Handler for SET Relay REST event
class SetRelay(resource.Resource):
    isLeaf=True
    def render_GET(self, request):
        if('v' in request.args and 'r' in request.args):
            r=int(request.args['r'][0])
            v=int(request.args['v'][0])
            if(r>0 and r<9 and (v==0 or v==1)):
                msk=1<<(r-1)
                if (v==1):cmd=0x11
                if (v==0):cmd=0x12
                data=packet(cmd,msk,0x00,0x00)
                SerialPort.write(port,data)
                print ">"+pk2str(data)
            else:
                print "r or v out of range"
        else:
            print "r or v missing"
        request.setHeader("content-type", "application/json")
        return json.dumps([Relay,Sensor])

# Handler for Test Relay Status REST event
class TestRelay(resource.Resource):
    isLeaf=True
    def render_GET(self, request):
        data=packet(0x18,0x00,0x00,0x00)
        SerialPort.write(port,data)
        request.setHeader("content-type", "application/json")
        request.setHeader("Cache-Control", "no-cache")
        return json.dumps([Relay,Sensor])

# REST Router tree    
if __name__ == "__main__":
    root = static.File(".")
    root.indexNames=['index.html']
root.putChild("set",SetRelay())
root.putChild("test",TestRelay())

# HTTP Server construct and start
factory = server.Site(root)
reactor.listenTCP(port, factory)

# Serial construct and start
port=SerialPort(SerLog(), serdev, reactor, baudrate=baud)

# Start event driven process
print "Reactor ready"
reactor.run()
