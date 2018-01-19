from executors import conf
import time


class DS18B20(object):
    def __init__(self):
        pass

    def run(self):
        while True:
            print(conf.aaa)
            time.sleep(1)
