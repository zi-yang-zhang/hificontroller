from protocol.goldmund import standby, setInput, setVolume, baudrate, query, standby_command, parseResponse, volume, volume_command, isSuccess, input_command
from hifiController import Peripheral
from device import Device
from hifiLogger import logger
# Goldmund设备策略
# 主设备开时开设备，并调节到频道7，音量85

AV_INPUT = 7
AV_VOLUME = 75
class GoldmundStrategy:
    def __init__(self, device: Device) -> None:
        self.__device__ = device
        self.checkAndSetStatus()
        pass

    def onMainDevicePowerOff(self):
        self.restoreStatus()
        pass

    def onMainDevicePowerOn(self):
        logger.info("Main device is on, try setInput to {} and setVolume to {}", AV_INPUT, AV_VOLUME)
        if self.__standby:
            logger.info("Goldmund is off, turining it on")
            code, result = self.send(standby(False))
            logger.debug("Standby result: {}", code)
            if not isSuccess(code):
                logger.error("Standby command failed {},{}", code, result)
                return
        if self.__input != AV_INPUT:
            code, result = self.send(input(AV_INPUT))
            logger.debug("Set Input result: {}", code)
        if self.__volume != AV_VOLUME:
            code, result = self.send(volume(AV_VOLUME))
            logger.debug("Set Volume result: {}", code)
        pass

    def restoreStatus(self):
        logger.info("Restoring status for goldmund: standby {}, input {}, volume {}", self.__standby, self.__input, self.__volume)
        # 本来是关的就关掉
        if self.__standby:
            code, result = self.send(standby(self.__standby))
        logger.debug("Set standby result: {}", code)
        if self.__volume != AV_VOLUME:
            code, result = self.send(volume(self.__volume))
            logger.debug("Set Volume result: {}", code)
        if self.__input != AV_INPUT:
            code, result = self.send(input(self.__input))
            logger.debug("Set Input result: {}", code)
    
    def checkAndSetStatus(self):
        code, standbyStatus = self.send(query(standby_command))
        if not isSuccess(code):
            logger.error("Query failed {},{}", code, standbyStatus)
            return
        command, status = standbyStatus.split(" ")
        code, input = self.send(query(input_command))
        if not isSuccess(code):
            logger.error("Query failed {},{}", code, input)
            return
        command, inputNumber = input.split(" ")
        code, volume = self.send(query(volume_command))
        if not isSuccess(code):
            logger.error("Query failed {},{}", code, volume)
            return
        command, volumeNumber = volume.split(" ")
        self.__input = inputNumber
        self.__standby = status == "on"
        self.__volume = volumeNumber
        logger.info("Current status for goldmund: standby {}, input {}, volume {}", self.__standby, self.__input, self.__volume)
        return 


    def send(self, request):
        return self.__device__.send(request, True, parseResponse, terminalChar= ">")

class Goldmund(Peripheral):
    def __init__(self, channelNumber) -> None:
        super().__init__("Goldmund")
        self.setStrategy(GoldmundStrategy(Device(channelNumber, baudrate)))
