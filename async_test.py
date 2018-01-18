import asyncio


async def hello(name):
    return "Hello, {}!".format(name)
    a += 1


async def call_vasya(loop):
    print('its call vasya')
    print(await hello("Vasya"))
    print('its call vasya-2')


async def test_2(loop):
    print('its te')
    print(await hello("Vasya"))
    print('its call vasya-2')


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        print('its loop')
        loop.run_until_complete(call_vasya(loop))
        print('its its loop')
    finally:
        loop.close()


# loop.run_in_executer -- для синхронных методов
# https://www.youtube.com/watch?v=z4gKgEN3v2Q
# loop.stop() -- выход из цикла run_forever

