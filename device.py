
from cmath import log
from driver import config
from hifiLogger import logger
# 树莓派的设备抽象
# 这里通信是走rs232协议

class Device:
    def __init__(self, channelNumber, baudrate):
        logger.debug("Init device with channel %s and baudrate %s", channelNumber, baudrate)
        self.__channel__ = config.config(Baudrate=baudrate, dev = "/dev/ttySC{}".format(channelNumber - 1))
        self.__channel__.dev

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

    def sendWithTerminal(self, request, parser = None, terminalChar = "\n"):
        logger.debug("Send request: %s", request)
        self.__channel__.Uart_SendString(request)
        logger.debug("Wait for %s", terminalChar)
        response = self.__channel__.Uart_ReceiveStringUntil(terminalChar)
        logger.debug("Response: %s",response)
        if parser is None:
            return response
        return parser(response)

    def sendUntilTerminal(self, request, parser = None, terminalChar = "\n"):
        logger.debug("Send request: %s", request)
        self.__channel__.Uart_SendString(request)
        logger.debug("Wait for %s", terminalChar)
        current = ""
        response = ""
        while current != terminalChar:
            current = self.__channel__.Uart_ReceiveString(1)
            response += current
        logger.debug("Response: %s",response)
        if parser is None:
            return response
        return parser(response)

    def sendWithLines(self, request, parser = None, lines = 1):
        logger.debug("Send request: %s", request)
        self.__channel__.Uart_SendString(request)
        logger.debug("Wait for %s lines", lines)
        response = self.__channel__.Uart_ReceiveStringLines(lines)
        logger.debug("Response: %s",response)
        if parser is None:
            return response
        return parser(response)

    def getChannel(self):
        return self.__channel__