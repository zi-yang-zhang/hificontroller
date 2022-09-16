from protocol.goldmund import standby, setInput, setVolumn, baudrate, query, standby_command, parseResponse
from hifiController import Peripheral
from device import Device
from hifiLogger import logger
# Goldmund设备策略
# 主设备开时开设备，并调节到频道7，音量85


class GoldmundStrategy:
    def __init__(self, device) -> None:
        self.__device__ = device
        # self.wasOn = False
        pass

    def onMainDevicePowerOff(self):
        # if not self.wasOn:
        #     logger.debug(self.__device__.send(standby(False)), True)
        # self.wasOn = False
        pass

    def onMainDevicePowerOn(self):
        logger.info("Main device is on, try set input to 7 and volumn to 70")
        result = self.__device__.send(
            query(standby_command), True, parseResponse)
        if result[1] == "off":
            logger.debug(self.__device__.send(standby(True), True))
            self.wasOn = False
        else:
            self.wasOn = True
        logger.debug(result)
        # logger.info("Device was on %s", self.wasOn)
        logger.debug(self.__device__.send(setInput(7)))
        logger.debug(self.__device__.send(setVolumn(70)))
        pass


class Goldmund(Peripheral):
    def __init__(self, channelNumber) -> None:
        super().__init__("Goldmund")
        self.setStrategy(GoldmundStrategy(Device(channelNumber, baudrate)))
