
from hifiLogger import logger
import serial

class IR:
    def __init__(self) -> None:
        self.__irDevice__ = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

    def setVolumeByIR(self, currentVol, newVol):
        diff = currentVol - newVol
        if diff < 0:
            vol = diff * -1
            logger.debug("Volumn down by %d", vol)
            self.__irDevice__.write("{}:{}\n".format("2", vol).encode('ascii'))
        else:
            logger.debug("Volumn up by {}", diff)
            self.__irDevice__.write("{}:{}\n".format("1", diff).encode('ascii'))
        result = self.__irDevice__.readline()
        logger.debug("Volumn result %d", result.decode())


if __name__ == '__main__':
    try:
        currentVol = int(input("current volume: "))
        newVol = int(input("new volume: "))
        IR().setVolumeByIR(currentVol, newVol)
    except KeyboardInterrupt:
        logger.info("ctrl + c:")
        exit()
