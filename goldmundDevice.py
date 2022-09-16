from protocol.goldmund import standby, setInput, setVolume, baudrate, query, standby_command, parseResponse, volume_command
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
        logger.info("Main device is on, try setInput to 7 and setVolume to 70")
        result = self.__device__.send(
            query(standby_command), True, parseResponse)
        logger.debug(result)
        logger.debug(self.__device__.send(standby(False), True, parseResponse))
        logger.debug(self.__device__.send(query(volume_command), True))
        # logger.info("Device was on %s", self.wasOn)
        logger.debug(self.__device__.send(setInput(7),True, parseResponse))
        logger.debug(self.__device__.send(setVolume(70),True, parseResponse))
        pass


class Goldmund(Peripheral):
    def __init__(self, channelNumber) -> None:
        super().__init__("Goldmund")
        self.setStrategy(GoldmundStrategy(Device(channelNumber, baudrate)))
