from hifiLogger import logger
from socketserver import ThreadingUDPServer, DatagramRequestHandler
from avSignalResponder import AVSignalResponder
from hifiController import Controller
# from goldmundDevice import Goldmund
import threading
import urllib3

CALL_TIME_INTERVAL = 300  # seconds

# Yamaha控制中心
# 用于注册Yamaha事件监听，以及对注入的controller做对应的响应


class YamahaControlServer:
    def __init__(self, yamahaHost, eventPort, controller: Controller = None) -> None:
        self.__host__ = yamahaHost
        self.__port__ = eventPort

        class DelegatingRequestHandler(DatagramRequestHandler):
            def handle(self):
                self.server.__deledating_handler__.handle(self)
        self.__server__ = ThreadingUDPServer(
            ('', self.__port__), DelegatingRequestHandler)
        self.__server__.__deledating_handler__ = AVSignalResponder(controller)
        pass

    def triggerYamahaEvent(self):
        try:
            logger.info("call server")
            http = urllib3.PoolManager()
            response = http.request('GET', self.__host__ + '/YamahaExtendedControl/v1/system/getDeviceInfo', headers={'X-AppName': 'MusicCast/1.0(YamahaControlServer)',
                                                                                                                    'X-AppPort': self.__port__})
            logger.info(response.data)
        except Exception as err:
            logger.error("trigger error: {0}", err)


    def startYamahaEventTrigger(self):
        self.triggerYamahaEvent()

        class RepeatTimer(threading.Timer):
            def run(self):
                while not self.finished.wait(self.interval):
                    self.function(*self.args, **self.kwargs)
        timer = RepeatTimer(CALL_TIME_INTERVAL, self.triggerYamahaEvent)
        timer.daemon = True
        timer.start()

    def startServer(self):
        logger.info("Starting server on thread %s", threading.get_native_id())
        self.startYamahaEventTrigger()
        self.__server__.serve_forever()
