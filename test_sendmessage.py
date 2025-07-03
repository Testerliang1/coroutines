import json
import re

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


async def main(data_list:list, method:str, base_url:str, login_url:str, login_data:dict, my_header=None):
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
            loginPayload = json.dumps(login_data)
            new_loginPayload = re.findall(r'#(.*?)#', loginPayload)
            for i in new_loginPayload:
                loginPayload = loginPayload.replace(f'#{i}#', f'{account}')
            loginPayload = json.loads(loginPayload)
            # 请求头
            head = my_header
            tasks.append(fetch(session,method=method, url=base_url + login_url, playload=loginPayload, header=head))
        results = await asyncio.gather(*tasks)
        # 写入文件
        for result in results:
            # with open('result.txt','a+') as f:
            #     f.write(f'{result}\n')
            # with open('token.txt','a+') as f:
            #     f.write(f'{result['data']['token']}\n')
            # with open('uid.txt','a+') as f:
            #     f.write(f'{result['data']['userInfo']['uid']}\n')
            print(f'response result: {result}')

def coroutines_reuqest(data_list_final:list, my_method:str, base:str, api_url:str, request_data:dict, header1=None):
    asyncio.run(main(data_list=data_list_final, method=my_method, base_url=base, login_url=api_url, login_data=request_data,
                     my_header=header1))

if __name__ == '__main__':
    user_list = ['100044752', '100044753']
    data_list = read_txt('user.txt')
    request_method = 'post'
    base = "http://47.83.162.112"
    url = "/api/im/session/send_message"
    login_data = {
        "content": "{\"emotionId\":34}",
        "fromUid":100047493, #100044752
        "isIncludeSender": 1,
        "messageType": "app:emotion",
        "target": "#man#" #100046401
    }
    header = {
        "token": "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxZmNjZWU0OS04NDNjLTRhZDEtOGI1Yy05ODJlZmM1OWNiNGEiLCJpYXQiOjE3NTA4NDM1NDQsImlzcyI6IndlcGFydHktZ2F0ZXdheSIsInN1YiI6IntcInVpZFwiOjEwMDA0NTg4MyxcImNvdW50cnlcIjpcIkNOXCIsXCJSZWdpb25cIjpcIkNOXCJ9IiwiZXhwIjoxNzUzNDM1NTQ0fQ.Xo-eZP-AVNrUHtHcYIhhLeMFj-sfsue9pWuZvcd-m6s",
        "device_id": "4e74efec-189b-47d6-b096-7b3529746e67",
        "new_device_id": "11009",
        "package_name": "com.partyjoy.yoki",
        "version_code": "17",
        "language_code": "zh",
        "lang_country_code": "CN",
        "country_code": "CN",
        "region": "CN",
        "device": "Android",
        "platform": "android",
        "channel": "google-play",
        "from_page": "com.adealink.weparty.message.conversation.ConversationActivity",
        "req_id": "bbd84549-f460-480f-b328-a2fadf98320f",
        "app_name": "yoki",
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "47.83.162.112",
        "User-Agent": "okhttp/4.12.0"
    }
    coroutines_reuqest(data_list_final=data_list[:50], my_method=request_method, base=base, api_url=url, request_data=login_data,
                     header1=header)
    # with open('token.txt','a+') as f:
    #     f.write('11111')
