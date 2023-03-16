import asyncio


# another custom coroutine
async def new_coro(message):
    await asyncio.sleep(2)
    # return the message
    return message


# custom coroutine
async def custom_coro(message):
    # wrap the coroutine in a task and schedule for execution
    task = asyncio.create_task(new_coro(message))

    # wait for the task to complete
    await task

    # it's done?
    print(task.done())

    # get the rask result
    print(task.result())

    # add hooks when the task / coroutine is marked as done
    task.add_done_callback(lambda t: print(f'Do something on {t.__class__} done!'))


# beers coroutine <async_generator>
async def generator_coro(beers: int):
    for message in ['Hello', 'Python', 'Coruña', "Let's", 'take', 'at least', beers, 'beers']:
        await asyncio.sleep(1)
        yield message


async def coroutine_with_generators(beers: int):
    # iterate over async generator using async over loop
    async for msg in generator_coro(beers):
        print(msg)


# create and execute coroutine
asyncio.run(custom_coro('Hi from a coroutine'))
asyncio.run(coroutine_with_generators(beers=3))
