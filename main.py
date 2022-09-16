import os
import sys
from hifiLogger import logger
from controlServer import YamahaControlServer
from goldmundDevice import Goldmund
from hifiController import Controller

PORT = 5005
YAMAHA_HOST = 'http://192.168.50.119'

driverDir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'driver')
if os.path.exists(driverDir):
    sys.path.append(driverDir)
protocolDir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'protocol')
if os.path.exists(protocolDir):
    sys.path.append(protocolDir)


if __name__ == '__main__':
    try:
        controller = Controller()
        controller.addPeripheral(Goldmund(1))
        server = YamahaControlServer(YAMAHA_HOST, PORT, controller)
        server.startServer()
        
    except KeyboardInterrupt:
        logger.info("ctrl + c:")
        exit()
