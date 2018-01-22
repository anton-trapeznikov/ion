from service import ServiceContext
from settings import config
import glob
import json
import time
import os


class DS18B20(ServiceContext):
    def __init__(self):
        super(DS18B20, self).__init__()

        self.sensors = {}
        print('-' * 20)
        print(config.W1_DEVICE_FOLDER)
        pattern = os.path.join(config.W1_DEVICE_FOLDER, '28-*')
        for path in glob.glob(pattern):
            sensor_id = os.path.basename(os.path.normpath(path))
            self.sensors[sensor_id] = os.path.join(path, 'w1_slave')

        self.can_work = True

    def read_temperature(self, sensor_id):
        result = None
        with open(self.sensors[sensor_id]) as f:
            cell = [l for l in f.readlines() if 't=' in l][0]
            if cell:
                result = cell.split('t=')[-1]

        result = float(result) * 0.001 if result else None
        return result

    def start(self):
        while self.can_work:
            for sensor_id in self.sensors:
                '''
                self.publish(
                    config.CHANNEL_MAP['ds18b20'],
                    json.dumps({
                        'timestamp': time.time(),
                        'id': sensor_id,
                        'value': self.read_temperature(sensor_id),
                    }),
                )'''
                print(sensor_id, self.read_temperature(sensor_id))

            time.sleep(1)
