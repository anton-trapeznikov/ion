import redis
import ionmq

if __name__ == "__main__":
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)

    broker = ionmq.IonMQBroker(redis=r)
    broker.start()
