import asyncio

from asyncio import Queue


async def do_work(task_name, work_queue):
    while not work_queue.empty():
        print('-'*10)
        print(work_queue)
        queue_item = work_queue.get_nowait()
        print(work_queue)
        # simulate condition where task is added dynamically
        #if queue_item % 2 != 0:
        work_queue.put_nowait(2)
            #print('Added additional item to queue')

        #print('{0} got item: {1}'.format(task_name, queue_item))
        await asyncio.sleep(queue_item)
        #print('{0} finished processing item: {1}'.format(task_name, queue_item))

if __name__ == '__main__':

    queue = Queue()

    # Load initial jobs into queue
    [queue.put_nowait(x) for x in range(1, 5)]

    # use 3 workers to consume tasks
    taskers = [
        do_work('task1', queue),
        do_work('task2', queue),
        do_work('task3', queue)
    ]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(taskers))
    loop.close()
