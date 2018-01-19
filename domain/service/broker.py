from service import ServiceMixin
import ionmq


class MQBroker(ServiceMixin, ionmq.IonMQBroker):
    def __init__(self):
        self.set_process_title()
        super(MQBroker, self).__init__(
            redis=self.get_redis_connection(),
        )
