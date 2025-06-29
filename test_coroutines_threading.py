import requests

import aiohttp
import asyncio

from datetime import datetime

async def fetch(session, url):
    async with session.get(url) as response:
        return response.status, len(await response.text())

async def main(i=1):
    """
    :param i: 异步请求
    :return:
    """
    start_time = int(datetime.now().timestamp() * 1000)
    urls = ['https://www.baidu.com/'] * i
    print("百度：{}".format(urls[0]))

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        for status, length in results:
            # print(f'URL status: {status}, Content length: {length}')
            pass

    stop_time = int(datetime.now().timestamp() * 1000)

    print(f'asyncio异步请求{i}次百度，总耗时: {stop_time - start_time}ms')
    return stop_time - start_time

def ordinary_request(i=1):
    start_time = int(datetime.now().timestamp() * 1000)
    urls = ['https://www.baidu.com/'] * i
    for url in urls:
        response = requests.get(url)
        # print(f'URL status: {response.status_code}, Content length: {len(response.text)}')
    stop_time = int(datetime.now().timestamp() * 1000)
    print(f'for循环同步请求{i}次百度，总耗时: {stop_time - start_time}ms')
    return stop_time - start_time


if __name__ == '__main__':
    asyncio_time = asyncio.run(main(100))
    for_time = ordinary_request(100)
    print()
    print(f'异步比同步请求效率快了{round(for_time / asyncio_time, 2)}倍')