from hifiLogger import logger

class Strategy:
    def onMainDevicePowerOn(self):
        pass

    def onMainDevicePowerOff(self):
        pass

# 周边设备控制器能力，会响应主设备开关
class PeripheralController:
    def onMainDevicePowerOn(self):
        self.__strategy__.onMainDevicePowerOn()
        logger.debug(format("%s onMainDevicePowerOn", self.__name__))

    def onMainDevicePowerOff(self):
        self.__strategy__.onMainDevicePowerOff()
        logger.debug(format("%s onMainDevicePowerOff", self.__name__))

# 周边设备定义，用于设置对应的策略，目前是响应主设备开关
class Peripheral(PeripheralController):
    def __init__(self, name) -> None:
        super().__init__()
        self.__name__ = name
    def setStrategy(self, strategy:Strategy):
        self.__strategy__ = strategy

# 控制器，可以添加周边设备，并触发周边设备对应的控制能力
class Controller(object):
    def __init__(self) -> None:
        self.__peripherals__ = []
        pass

    def addPeripheral(self, peripheral: Peripheral):
        self.__peripherals__.append(peripheral)

    def onPowerOn(self):
        for p in self.__peripherals__:
            p.onMainDevicePowerOn()

    def onPowerOff(self):
        for p in self.__peripherals__:
            p.onMainDevicePowerOn()
