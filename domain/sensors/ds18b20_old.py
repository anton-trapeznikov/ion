from service import ServiceContext
from settings import config
import aiofiles
import asyncio
# import uvloop
import signal
import glob
import json
import time
import os


class DS18B20(ServiceContext):
    def __init__(self):
        super(DS18B20, self).__init__()

        self.sensors = {}
        pattern = os.path.join(config.W1_DEVICE_FOLDER, '28-*')
        for path in glob.glob(pattern):
            sensor_id = os.path.basename(os.path.normpath(path))
            self.sensors[sensor_id] = os.path.join(path, 'w1_slave')

        self.can_work = True

    async def fetch_temperature(self):
        while not self.queue.empty():
            value = None
            sensor_id = await self.queue.get()

            async with aiofiles.open(self.sensors[sensor_id], mode='r') as f:
                contents = await f.readlines()
                cell_rows = [l for l in contents if 't=' in l]
                if cell_rows:
                    value = cell_rows[0].split('t=')[-1]

            value = float(value) * 0.001 if value else None

            self.publish(
                config.CHANNEL_MAP['ds18b20'],
                json.dumps({
                    'timestamp': time.time(),
                    'id': sensor_id,
                    'value': self.read_temperature(sensor_id),
                }),
            )

            await asyncio.sleep(config.DS18B20_FETCH_DELAY)
            if self.can_work:
                self.queue.put_nowait(sensor_id)

    def stop(self):
        self.can_work = False

    def start(self):
        if not self.sensors:
            return

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        # self.loop = asyncio.get_event_loop()

        self.loop.add_signal_handler(signal.SIGINT, self.stop)
        self.loop.add_signal_handler(signal.SIGTERM, self.stop)

        self.queue, workers = asyncio.Queue(), []

        for sensor_id in self.sensors:
            self.queue.put_nowait(sensor_id)
            workers.append(
                asyncio.ensure_future(self.fetch_temperature())
            )

        self.loop.run_until_complete(asyncio.wait(workers))
        self.loop.close()
