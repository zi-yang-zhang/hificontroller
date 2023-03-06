
from hifiLogger import logger
import serial, time

class IR:
    def __init__(self) -> None:
        self.__irDevice__ = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.__irDevice__.reset_input_buffer()
        self.__irDevice__.reset_output_buffer()
        time.sleep(0.1) #wait for serial to open

    def setVolumeByIR(self, currentVol, newVol):
        diff = newVol - currentVol
        cmd = ""
        if diff < 0:
            vol = diff * -1
            cmd = "{}:{}\n".format("2", vol)
            logger.debug("Volumn down by %d", vol)
        else:
            logger.debug("Volumn up by %d", diff)
            cmd = "{}:{}\n".format("1", diff)
        logger.debug("cmd:%s", cmd)
        logger.debug("writable:%s", self.__irDevice__.writable)
        
        sent = self.__irDevice__.write(cmd.encode('utf-8'))        
        logger.debug("sent:%d", sent)
    
        while True:
            sent = self.__irDevice__.write(b'1\n')        
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
