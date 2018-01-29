from abc import ABCMeta, abstractmethod
from setproctitle import setproctitle
from settings import config
import signal
import redis
import ionmq
import time


class DaemonContext(object):
    __metaclass__ = ABCMeta

    def __init__(self, loop_delay=None, process_title=None):
        self.redis = self.get_redis_connection()
        self.set_process_title(title=process_title)
        self.loop_delay = float(loop_delay or config.DEFAULT_LOOP_DELAY)
        for s in (signal.SIGINT, signal.SIGTERM):
            signal.signal(s, self.stop)

        self.can_work = True

    def get_redis_connection(self):
        pool = redis.ConnectionPool(
            host=config.REDIS['host'],
            port=config.REDIS['port'],
            db=config.REDIS['db'],
        )

        return redis.Redis(connection_pool=pool)

    @abstractmethod
    def payload(self):
        raise NotImplementedError('Abstract method raise')

    def start(self):
        while self.can_work:
            self.payload()
            time.sleep(self.loop_delay)

        self.clean()

    def stop(self, signum=None, frame=None):
        self.can_work = False

    def clean(self):
        pass

    @property
    def default_process_title(self):
        return 'ion-service:%s' % self.__class__.__name__.lower()

    def set_process_title(self, title=None):
        self.process_name = title or self.default_process_title
        setproctitle(self.process_name)


class ServiceMixin(object):
    def get_redis_connection(self):
        pool = redis.ConnectionPool(
            host=config.REDIS['host'],
            port=config.REDIS['port'],
            db=config.REDIS['db'],
        )

        return redis.Redis(connection_pool=pool)

    @property
    def default_process_title(self):
        return 'ion-%s' % self.__class__.__name__.lower()

    def set_process_title(self, title=None):
        setproctitle(title or self.default_process_title)


class ServiceContext(ionmq.IonMQClient, ServiceMixin):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.set_process_title()
        self.redis = self.get_redis_connection()
        super(ServiceContext, self).__init__(
            imq_client_id=self.default_process_title,
            redis=self.get_redis_connection(),
        )

    @abstractmethod
    def start(self):
        raise NotImplementedError('Abstract method raise')
