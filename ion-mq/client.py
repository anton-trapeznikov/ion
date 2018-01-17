from ionmq import IonMQClient
import redis
import json
import time


channel_1 = 'T1'
channel_2 = 'T2'

id_1 = 'cli_1'
id_2 = 'cli_2'
id_3 = 'cli_3'

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)


class Client(IonMQClient):
    def default_handler(self, message):
        message = json.loads(message)

        print(
            "[x] I'm %s.Received %s. Channel %s from %s" % (
                self.imq_client_id,
                message.get('message'),
                message.get('channel'),
                message.get('client')
            )
        )


tester_1 = Client(imq_client_id=id_1, redis=r)
tester_2 = Client(imq_client_id=id_2, redis=r)
tester_3 = Client(imq_client_id=id_3, redis=r)

tester_1.subscribe(channel_1, tester_1.default_handler)
tester_2.subscribe(channel_1, tester_2.default_handler)

tester_3.publish(channel_1, 'test_message')
time.sleep(1)

tester_1.listen()
tester_2.listen()

tester_2.unsubscribe_from_all()
tester_3.publish(channel_1, 'test_message-2')
time.sleep(1)

tester_1.listen()
tester_2.listen()
