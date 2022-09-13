from protocol.dac8dsd import power, baudrate, parseResponse
from device import Device
from hifiController import Peripheral
from hifiLogger import logger

# T+ADAC8DSD策略
# 主设备开关时发送开关指令

class TADac8DSDStrategy:
    def __init__(self, device: Device) -> None:
        self.__device__ = device
        pass

    def onMainDevicePowerOff(self):
        logger.debug(self.__device__.send(power(False), True, parseResponse))
        pass

    def onMainDevicePowerOn(self):
        logger.debug(self.__device__.send(power(True), True, parseResponse))
        pass

    def getDevice(self):
        return self.__device__


class TADac8DSD(Peripheral):
    def __init__(self, channelNumber) -> None:
        super().__init__("T+A DAC8 DSD")
        self.setStrategy(TADac8DSDStrategy(Device(channelNumber, baudrate)))

    def getDevice(self):
        return self.__strategy__.getDevice()
