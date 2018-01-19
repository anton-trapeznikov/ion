import asyncio


async def handle_exception():
    try:
        await bug()
    except Exception:
        print('TADA!')

async def bug():
    raise Exception()

loop = asyncio.get_event_loop()
loop.create_task(handle_exception())
loop.run_forever()
loop.close()
