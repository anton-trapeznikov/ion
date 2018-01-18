import asyncio
import signal
import os

can_work = True


async def do_work(loop):
    while can_work:
        await asyncio.sleep(1, loop=loop)

    print('===' * 20)


def signal_handler(loop):
    loop.remove_signal_handler(signal.SIGTERM)
    can_work = False


loop = asyncio.get_event_loop()
loop.add_signal_handler(signal.SIGTERM, signal_handler, loop)
print(os.getpid())
loop.run_until_complete(do_work(loop))
