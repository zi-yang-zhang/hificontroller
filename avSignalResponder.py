from socketserver import DatagramRequestHandler
import json
from hifiLogger import logger
from hifiController import Controller
# 环绕信号控制器
# 目前只对开关信号响应
class AVSignalResponder:
    def __init__(self, controller: Controller) -> None:
        self.__controller__ = controller
        pass

    def onPowerOn(self):
        if self.__controller__ is not None:
            self.__controller__.onPowerOn()
        return

    def onPowerOff(self):
        if self.__controller__ is not None:
            self.__controller__.onPowerOff()
        return

    def handle(self, handler: DatagramRequestHandler):
        logger.debug('Got connection from', handler.client_address[0][0])
        msg, sock = handler.request
        # logger.debug(msg)
        response = json.loads(msg) 
        if "main" in response:
            if "power" in response["main"]:
                status = response["main"]["power"]
                logger.debug("yamaha power status: %s" % status)
                if status == "on":
                    self.onPowerOn()
                if status == "standby":
                    self.onPowerOff()