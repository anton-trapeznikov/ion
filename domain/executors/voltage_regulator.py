from abc import ABCMeta, abstractmethod
from settings import config


class Heater(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.min_voltage = config.MIN_VOLTAGE_REGULATOR_OUTPUT
        self.max_voltage = config.MAX_VOLTAGE_REGULATOR_OUTPUT
        self.__output_voltage = None
        self.output_voltage = 0

    @abstractmethod
    def on(self):
        raise NotImplementedError('Abstract method raise')

    @abstractmethod
    def off(self):
        raise NotImplementedError('Abstract method raise')

    @abstractmethod
    @property
    def is_on(self):
        raise NotImplementedError('Abstract method raise')

    @abstractmethod
    @property
    def is_off(self):
        raise NotImplementedError('Abstract method raise')

    @abstractmethod
    @property
    def output_voltage(self):
        raise NotImplementedError('Abstract method raise')

    @abstractmethod
    @output_voltage.setter
    def output_voltage(self, output_voltage):
        raise NotImplementedError('Abstract method raise')