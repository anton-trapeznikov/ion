from service import ServiceContext
import asyncio
import signal


class DS18B20(ServiceContext):
    async def fetch(self, file_path):
        print('[X] reading %s' % file_path)
        with open(file_path) as f:
            data = f.read()
            print('[X] read %s' % data)

    def signal_handler(loop):
        loop.remove_signal_handler(signal.SIGTERM)
        loop.stop()

    def start(self):
        files = [
            '/home/anton/devel/1.txt', '/home/anton/devel/3.txt',
            '/home/anton/devel/2.txt', '/home/anton/devel/4.txt'
        ]

        loop = asyncio.get_event_loop()
        loop.add_signal_handler(
            signal.SIGTERM,
            self.signal_handler,
            loop
        )

        for f in files:
            asyncio.async(self.fetch(file_path=f))

        loop.run_forever()
        loop.close()
