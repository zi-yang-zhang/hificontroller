import logging
import sys

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logging.basicConfig(
    # filename='./log/server.log',
    #                 filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    handlers=[handler],
                    level=logging.DEBUG)

logger = logging.getLogger('hifiController')