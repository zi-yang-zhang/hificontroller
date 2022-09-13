
from driver import config
from hifiLogger import logger
# 树莓派的设备抽象
# 这里通信是走rs232协议

class Device:
    def __init__(self, channelNumber, baudrate):
        self.__channel__ = config.config(Baudrate=baudrate, dev = "/dev/ttySC{}".format(channelNumber - 1))

    def send(self, request, needResponse = False, parser = None, bufferSize = 26):
        logger.debug("Send request %s", request)
        self.__channel__.Uart_SendString(request)
        if needResponse: 
            response = self.__channel__.Uart_ReceiveString(bufferSize)
            logger.debug("Response:%s",response)
            if parser is None:
                return response
            return parser(response)
        return "No response"
        
    def getChannel(self):
        return self.__channel__