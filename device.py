
from driver import config

# 树莓派的设备抽象
# 这里通信是走rs232协议

class Device:
    def __init__(self, channelNumber, baudrate):
        self.__channel__ = config.config(Baudrate=baudrate, dev = "/dev/ttySC{}".format(channelNumber - 1))

    def send(self, request, needResponse = False, parser = None, bufferSize = 26):
        self.__channel__.Uart_SendString(request)
        if needResponse: 
            if parser is None:
                return self.__channel__.Uart_ReceiveString(bufferSize)
            return parser(self.__channel__.Uart_ReceiveString(bufferSize))
        return "No response"
        
    def getChannel(self):
        return self.__channel__