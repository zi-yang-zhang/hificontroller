
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
            self.__irDevice__.write("{}:{}\n".format("2", vol).encode())
        else:
            logger.debug("Volumn up by %d", diff)
            self.__irDevice__.write("{}:{}\n".format("1", diff).encode())
        while True:
            if self.__irDevice__.in_waiting > 0:
                line = self.__irDevice__.readline().decode('utf-8').rstrip()
                logger.debug(line)


if __name__ == '__main__':
    try:
        currentVol = int(input("current volume: "))
        newVol = int(input("new volume: "))
        IR().setVolumeByIR(currentVol, newVol)
    except KeyboardInterrupt:
        logger.info("ctrl + c:")
        exit()
