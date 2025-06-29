import aiohttp
import asyncio

import uuid
import random


def read_txt(file_path):
    all_lines = []
    # 打开并读取txt文件
    with open(file_path, 'r', encoding='utf-8') as file:
        # 遍历每一行
        for line in file:
            # 去除每行前后的空格，并将每行按空格分割成单词
            words = line.strip()
            # 将分割后的单词列表添加到all_lines列表中
            all_lines.append(words)

    return all_lines

async def fetch(session, method:str, url:str, playload, header=None):
    if header:
        if method.upper() == 'POST':
            async with session.post(url,headers=header,json=playload) as response:
                response_json = await response.json()  # 获取响应的 JSON 数据
                if response.status != 200:
                    raise Exception(f"请求失败，状态码: {response.status}, 响应内容: {response_json}")
                return response_json
        elif  method.upper() == 'GET':
            async with session.get(url,headers=header,data=playload) as response:
                response_json = await response.json()  # 获取响应的 JSON 数据
                if response.status != 200:
                    raise Exception(f"请求失败，状态码: {response.status}, 响应内容: {response_json}")
                return response_json
        return None
    else:
        if method.upper() == 'POST':
            async with session.post(url,json=playload) as response:
                response_json = await response.json()  # 获取响应的 JSON 数据
                if response.status != 200:
                    raise Exception(f"请求失败，状态码: {response.status}, 响应内容: {response_json}")
                return response_json
        elif  method.upper() == 'GET':
            async with session.get(url,data=playload) as response:
                response_json = await response.json()  # 获取响应的 JSON 数据
                if response.status != 200:
                    raise Exception(f"请求失败，状态码: {response.status}, 响应内容: {response_json}")
                return response_json
        return None


async def main(data_list:list, method:str, base_url:str, login_url:str, my_header=None):
    """
    :param my_header: 请求头
    :param method: 请求方式
    :param base_url: 域名
    :param login_url: 接口api
    :param data_list: 循环数据列表
    :return:
    """

    async with aiohttp.ClientSession() as session:
        # tasks = [fetch(session, url) for url in urls]
        tasks = []
        for account in data_list:
            # 请求参数
            loginPayload = {
                "accessToken": "",
                "lang": "zh",
                "appsflyerId": f"{uuid.uuid1()}",
                "channel": "google-play",
                "country": "NG",
                "deviceId": f"{uuid.uuid1()}",
                "deviceToken": f"{uuid.uuid1()}",
                "fbAccount": f"{account}",
                "newDeviceId": f"{random.randint(1000, 99999)}",
                "packageName": "com.partyjoy.yoki",
                "platform": "android",
                "seqid": 0,
                "simMcc": "",
                "fromSimulator": False,
                "systemLang": "zh",
                "thirdType": "fb",
                "versionCode": 3,
                "virtualApk": False
            }
            # 请求头
            head = my_header
            tasks.append(fetch(session,method=method, url=base_url + login_url, playload=loginPayload, header=head))
        results = await asyncio.gather(*tasks)
        # 写入文件
        for result in results:
            # with open('result.txt','a+') as f:
            #     f.write(f'{result}\n')
            with open('token.txt','a+') as f:
                f.write(f'{result['data']['token']}\n')
            with open('uid.txt','a+') as f:
                f.write(f'{result['data']['userInfo']['uid']}\n')
            print(f'response result: {result}')


if __name__ == '__main__':
    request_method = 'post'
    base = "http://47.83.162.112"
    url = "/api/account/login"
    user_list = ['19982060', '19982061']
    asyncio.run(main(data_list=user_list, method=request_method, base_url=base, login_url=url,
                     my_header=None))
    # with open('token.txt','a+') as f:
    #     f.write('11111')
