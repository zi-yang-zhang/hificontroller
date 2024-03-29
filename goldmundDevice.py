from protocol.goldmund import standby, setInput, setVolume, volumeUp, baudrate, query, standby_command, parseResponse, volume_command, isSuccess, input_command
from hifiController import Peripheral
from device import Device
from hifiLogger import logger
import serial, time

# Goldmund设备策略
# 主设备开时开设备，并调节到频道7，音量85

AV_INPUT = "5"
AV_VOLUME = 85
VOL_UP = "1"
VOL_DOWN = "2"
MAX_RETRY = 20

class GoldmundStrategy:
    def __init__(self, device: Device) -> None:
        self.__device__ = device
        self.__irDevice__ = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.__irDevice__.reset_input_buffer()
        self.__irDevice__.reset_output_buffer()
        time.sleep(0.1) #wait for serial to open
        self.checkAndSetStatus()
        pass

    # 主设备关机的话就恢复之前状态
    def onMainDevicePowerOff(self):
        self.restoreStatus()
        pass

    # 当主设备开启时，先记录当前设备状态，然后再调整到AV配置，如果没开机的话先开机
    def onMainDevicePowerOn(self):
        logger.info(
            "Main device is on, try setInput to %s and setVolume to %s", AV_INPUT, AV_VOLUME)
        self.checkAndSetStatus()
        if self.__standby:
            logger.info("Goldmund is off, turining it on")
            code, result = self.send(standby(False))
            logger.debug("Standby result: %s", code)
            if not isSuccess(code):
                logger.error("Standby command failed %s,%s", code, result)
                return
        if self.__input != AV_INPUT:
            code, result = self.send(setInput(AV_INPUT))
            logger.debug("Set Input result: %s", code)
        if self.__volume != AV_VOLUME:
            self.setVolumeByIR(AV_VOLUME, int(self.__volume))
            logger.debug("Set Volume result")
        pass

    # 回复上一次状态，如果上一次的状态本来就跟AV状态一样则不变。如果上一次是standby的则会关机
    def restoreStatus(self):
        logger.info("Restoring status for goldmund: standby %s, input %s, volume %s",
                    self.__standby, self.__input, self.__volume)
        # 本来是关的就关掉
        if self.__standby:
            code, result = self.send(standby(self.__standby))
            logger.debug("Set standby result: %s", code)
            if isSuccess(code):
                return
        code, input = self.getInputStatus()
        if not isSuccess(code):
            return
        # 不在av频道就不回切了
        if input != AV_INPUT:
            logger.debug("Input already swiched %s, won't restore",input)
            return
        code, volume = self.getVolumneStatus()
        if not isSuccess(code):
            return
        if self.__volume != volume:
            self.setVolumeByIR(int(self.__volume), int(volume))
            logger.debug("Set Volume result")
        if self.__input != input:
            code, result = self.send(setInput(self.__input))
            logger.debug("Set Input result: %s", code)

    def getStandbyStatus(self):
        code, standbyStatus = self.send(query(standby_command))
        if not isSuccess(code):
            logger.error("Query failed %s,%s", code, standbyStatus)
            return code, ""
        command, status = standbyStatus.split(" ")
        return code, status
    def getInputStatus(self):
        code, input = self.send(query(input_command))
        if not isSuccess(code):
            logger.error("Query failed %s,%s", code, input)
            return code, ""
        command, inputNumber = input.split(" ")
        return code, inputNumber
    def getVolumneStatus(self):
        code, volumne = self.send(query(volume_command))
        if not isSuccess(code):
            logger.error("Query failed %s,%s", code, volumne)
            return code, ""
        command, volumeNumber = volumne.split(" ")
        return code, volumeNumber
    
    # 查看机器状态，将开关机/输入/音量记录下来
    def checkAndSetStatus(self):
        code, standbyStatus  = self.getStandbyStatus()
        if not isSuccess(code):
            return
        code, input = self.getInputStatus()
        if not isSuccess(code):
            return
        code, volume = self.getVolumneStatus()
        if not isSuccess(code):
            return
        self.__input = input
        self.__standby = standbyStatus == "on"
        self.__volume = volume
        logger.info("Current status for goldmund: standby %s, input %s, volume %s",
                    self.__standby, self.__input, self.__volume)
        return

    def setVolumeByIR(self, targetVol: int, curVol: int, retries: int=0):
        logger.debug("setVolumeByIR target:%d, currentVol:%d retries:%d",targetVol, curVol, retries)
        if retries == MAX_RETRY:
            logger.error("Max retried %s,%s", targetVol, retries)
            return
        diff = targetVol - curVol
        if diff == 0: return
        cmd = ""
        if diff < 0:
            vol = diff * -1
            cmd = VOL_DOWN + str(vol)
            logger.debug("Volumn down by %d", vol)
        else:
            logger.debug("Volumn up by %d", diff)
            cmd = VOL_UP + str(diff)
        logger.debug("Send ir command %s", cmd)
        sent = self.__irDevice__.write(cmd.encode('utf-8'))
        while  self.__irDevice__.in_waiting == 0: pass
        while self.__irDevice__.in_waiting > 0:
            result = self.__irDevice__.readline().decode('utf-8').rstrip()
            logger.debug("Volumn result %s", result)
        code, standbyStatus  = self.getStandbyStatus()
        if not isSuccess(code) or standbyStatus != "off":
            logger.debug("standbyStatus is not off: %s", standbyStatus)
            return
        code, volume = self.getVolumneStatus()
        if int(volume) != targetVol:
            logger.debug("Volumn not acurate %s, retry", volume)
            self.setVolumeByIR(targetVol, int(volume), retries + 1)

    def send(self, request):
        return self.__device__.sendUntilTerminal(request, parseResponse, ">")


class Goldmund(Peripheral):
    def __init__(self, channelNumber) -> None:
        super().__init__("Goldmund")
        self.setStrategy(GoldmundStrategy(Device(channelNumber, baudrate)))
