from abc import ABCMeta, abstractmethod
from setproctitle import setproctitle
from settings import config
import redis
import ionmq


class ServiceMixin(object):
    def get_redis_connection(self):
        pool = redis.ConnectionPool(
            host=config.REDIS['host'],
            port=config.REDIS['port'],
            db=config.REDIS['db'],
        )

        return redis.Redis(connection_pool=pool)

    @property
    def process_title(self):
        return 'ion-%s' % self.__class__.__name__.lower()

    def set_process_title(self):
        setproctitle(self.process_title)


class ServiceContext(ionmq.IonMQClient, ServiceMixin):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.set_process_title()
        super(ServiceContext, self).__init__(
            imq_client_id=self.process_title,
            redis=self.get_redis_connection(),
        )

    @abstractmethod
    def start(self):
        raise NotImplementedError('Abstract method raise')
