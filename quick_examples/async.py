import asyncio


async def nested():
    return 42


async def say_hello_asynchronously():
    for word in ['Hello', 'Python', 'Coruña', '2023']:
        yield word


async def main():
    print(f'Result not awaiting for the result {nested()}')
    print(f'Result awaiting for the result {await nested()}')

    sentence = ''
    async for word in say_hello_asynchronously():
        sentence += f'{word} '

    print(sentence)


asyncio.run(main())
