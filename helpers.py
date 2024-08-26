import asyncio


async def retry_helper(func, retries=3):
    result = None
    k = 0
    while not result and k < retries:
        result = await func()
        if not result:
            await asyncio.sleep(1)
        k += 1
    return result

