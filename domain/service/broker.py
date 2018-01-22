from service import ServiceMixin
from settings import config
import ionmq


class MQBroker(ServiceMixin, ionmq.IonMQBroker):
    def __init__(self):
        self.set_process_title()
        super(MQBroker, self).__init__(
            redis=self.get_redis_connection(),
            loop_delay=config.MQBROKER_LOOP_DELAY,
        )
