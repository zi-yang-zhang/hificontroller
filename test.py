
from hifiLogger import logger
import serial

class IR:
    def __init__(self) -> None:
        self.__irDevice__ = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

    def setVolumeByIR(self, currentVol, newVol):
        diff = currentVol - newVol
        if diff < 0:
            logger.debug("Volumn down by {}", diff * -1)
            self.__irDevice__.write(b"{}:{}\n".format("2", diff * -1))
        else:
            logger.debug("Volumn up by {}", diff)
            self.__irDevice__.write(b"{}:{}\n".format("1", diff))
        result = self.__irDevice__.readline()
        logger.debug("Volumn result {}", result)


if __name__ == '__main__':
    try:
        currentVol = int(input("current volume: "))
        newVol = int(input("new volume: "))
        IR().setVolumeByIR(currentVol, newVol)
    except KeyboardInterrupt:
        logger.info("ctrl + c:")
        exit()
