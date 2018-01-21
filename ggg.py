import asyncio
import signal
import multiprocessing
import functools
import random
import aiofiles
import time


class Test(object):
    def __init__(self):
        self.can_work = True

    def stop(self):
        self.can_work = False

    async def fetch_temperature(self):
        while not self.queue.empty():
            task = await self.queue.get()
            async with aiofiles.open(task, mode='r') as f:
                contents = await f.readlines()
                print(contents)

            await asyncio.sleep(random.randint(0, 10))
            if self.can_work:
                self.queue.put_nowait(task)

    def start(self):
        self.files = [
            '/home/anton/devel/1.txt',
            '/home/anton/devel/2.txt',
            '/home/anton/devel/3.txt',
            '/home/anton/devel/4.txt'
        ]
        self.loop = asyncio.get_event_loop()
        self.loop.add_signal_handler(signal.SIGINT, self.stop)
        self.loop.add_signal_handler(signal.SIGTERM, self.stop)

        self.queue, workers = asyncio.Queue(), []

        for f in self.files:
            self.queue.put_nowait(f)
            workers.append(
                asyncio.ensure_future(self.fetch_temperature())
            )

        self.loop.run_until_complete(asyncio.wait(workers))
        self.loop.close()


a = Test()
a.start()
