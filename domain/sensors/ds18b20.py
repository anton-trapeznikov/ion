from service import DaemonContext
from settings import config
import time
import os


class DS18B20(DaemonContext):
    def __init__(self, **kwargs):
        self.sensor_id = kwargs.get('entry_id', '')

        title = '%s-%s.d' % (self.default_process_title, self.sensor_id)
        super(self.__class__, self).__init__(process_title=title)

        self.data_file = os.path.join(
            config.W1_DEVICE_FOLDER, self.sensor_id, 'w1_slave')
        self.can_work = os.path.exists(self.data_file)

        self.redis_data_key = '%s%s' % (
            config.REDIS_KEY['ds18b20_value'], self.sensor_id)
        self.redis_timestamp_key = '%s%s' % (
            config.REDIS_KEY['ds18b20_timestamp'], self.sensor_id)
        self.redis_list_key = config.REDIS_KEY['ds18b20_ids']
        self.redis.sadd(self.redis_list_key, self.sensor_id)

    def payload(self):
        value = ''
        with open(self.data_file, mode='r') as f:
            contents = f.readlines()
            cell_rows = [l for l in contents if 't=' in l]
            if cell_rows:
                value = cell_rows[0].split('t=')[-1]

        value = float(value) * 0.001 if value else ''

        self.redis.set(self.redis_data_key, value)
        self.redis.set(self.redis_timestamp_key, time.time())

    def clean(self):
        self.redis.delete(self.redis_data_key)
        self.redis.delete(self.redis_timestamp_key)
        self.redis.spop(self.redis_list_key)
        super(self.__class__, self).clean()
