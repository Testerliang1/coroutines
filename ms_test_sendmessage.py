import json
import re
import sys
import aiohttp
import asyncio
import ast

from datetime import datetime


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

async def fetch(session, method:str, url:str, payload, header=None):
    if header:
        if method.upper() == 'POST':
            async with session.post(url,headers=header,json=payload) as response:
                response_json = await response.json()  # 获取响应的 JSON 数据
                if response.status != 200:
                    raise Exception(f"请求失败，状态码: {response.status}, 响应内容: {response_json}")
                return response_json
        elif  method.upper() == 'GET':
            async with session.get(url,headers=header,data=payload) as response:
                response_json = await response.json()  # 获取响应的 JSON 数据
                if response.status != 200:
                    raise Exception(f"请求失败，状态码: {response.status}, 响应内容: {response_json}")
                return response_json
        return None
    else:
        if method.upper() == 'POST':
            async with session.post(url,json=payload) as response:
                response_json = await response.json()  # 获取响应的 JSON 数据
                if response.status != 200:
                    raise Exception(f"请求失败，状态码: {response.status}, 响应内容: {response_json}")
                return response_json
        elif  method.upper() == 'GET':
            async with session.get(url,data=payload) as response:
                response_json = await response.json()  # 获取响应的 JSON 数据
                if response.status != 200:
                    raise Exception(f"请求失败，状态码: {response.status}, 响应内容: {response_json}")
                return response_json
        return None


async def main(my_data_list:list or int, method:str, base_url:str, login_url:str, my_login_data:dict, my_header=None, request_times=200):
    """
    :param my_data_list: 循环数据列表
    :param method: 请求方式
    :param base_url: 域名
    :param login_url: 接口api
    :param my_login_data: 请求参数
    :param my_header: 请求头
    :param request_times: 没有数据list时默认请求次数
    :return:
    """

    async with aiohttp.ClientSession() as session:
        # tasks = [fetch(session, url) for url in urls]
        if isinstance(my_data_list, int):
            request_times = my_data_list
        final_url = base_url + login_url
        tasks = []
        data_need_replace = len(re.findall(r'#.*?#', json.dumps(my_login_data)))
        header_need_replace = len(re.findall(r'#.*?#', json.dumps(my_header)))
        if data_need_replace > 0 and header_need_replace == 0:
            for account in my_data_list:
                # 请求参数替换
                login_payload = json.dumps(my_login_data)
                match_field = re.findall(r'#(.*?)#', login_payload)
                for i in match_field:
                    login_payload = login_payload.replace(f'#{i}#', f'{account}')
                login_payload = json.loads(login_payload)
                # 请求头
                head = my_header
                tasks.append(
                    fetch(session, method=method, url=final_url, payload=login_payload, header=head))
            results = await asyncio.gather(*tasks)
        elif data_need_replace == 0 and header_need_replace > 0:
            for account in my_data_list:
                # 请求头替换
                header_payload = json.dumps(my_header)
                match_field = re.findall(r'#(.*?)#', header_payload)
                for i in match_field:
                    header_payload = header_payload.replace(f'#{i}#', f'{account}')
                header_payload = json.loads(header_payload)
                tasks.append(
                    fetch(session, method=method, url=final_url, payload=my_login_data, header=header_payload))
            results = await asyncio.gather(*tasks)
        elif data_need_replace == 0 and header_need_replace == 0:
            tasks = [fetch(session, method=method, url=final_url, payload=my_login_data, header=my_header) for final_url in [final_url] * request_times]
            results = await asyncio.gather(*tasks)
        elif data_need_replace > 0 and header_need_replace > 0:
            raise Exception('不支持请求参数和请求头中同时存在#字符！！')
        else:
            raise Exception('未考虑到的特殊请求数据！！')
        # 写入文件
        for result in results:
            # with open('result.txt','a+') as f:
            #     f.write(f'{result}\n')
            # with open('token.txt','a+') as f:
            #     f.write(f'{result['data']['token']}\n')
            # with open('uid.txt','a+') as f:
            #     f.write(f'{result['data']['userInfo']['uid']}\n')
            print(f'response result: {result}')

def coroutines_reuqest(data_list_final:list or int, my_method:str, base_domain:str, api_url:str, request_data:dict, header1=None):
    # 参数格式校验
    if data_list_final is None:
        raise ValueError("data_list 不能为空")
    if data_list_final is not None:
        if not isinstance(data_list_final, list):
            if not isinstance(int(data_list_final), int):
                raise ValueError("data_list 必须是列表类型或者整数类型")
    if not isinstance(my_method, str) or my_method.upper() not in ['POST', 'GET']:
        raise ValueError("request_method 必须是 'POST' 或 'GET' 字符串")
    if not isinstance(base_domain, str):
        raise ValueError("base 必须是字符串类型")
    if not isinstance(api_url, str):
        raise ValueError("url 必须是字符串类型")
    if not isinstance(request_data, dict):
        raise ValueError("login_data 必须是字典类型")
    if header1 is not None:
        if not isinstance(header1, dict):
            raise ValueError("headers 必须是字典类型")

    asyncio.run(main(my_data_list=data_list_final, method=my_method, base_url=base_domain, login_url=api_url, my_login_data=request_data,
                     my_header=header1))


if __name__ == '__main__':
    # data_list = ['100044752', '100044753', '100044754', '100044755', '100044756', '100044757', '100044758']
    # data_list = read_txt('user.txt')
    # 请求示例：
    # ['100044752', '100044753', '100044754', '100044755', '100044756', '100044757', '100044758']
    # post
    # http://47.83.162.112
    # /api/im/session/send_message
    # {"content": "{\"emotionId\":34}", "fromUid": 100047838, "isIncludeSender": 1, "messageType": "app:emotion", "target": "#man#"}
    # {"token": "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI2ZmEyNmM4My1hM2E0LTQ3OTktOWVmZC05YmQzNWUyZDhlNmIiLCJpYXQiOjE3NTE5Njk1NTgsImlzcyI6IndlcGFydHktZ2F0ZXdheSIsInN1YiI6IntcInVpZFwiOjEwMDA0NzgzNixcIlJlZ2lvblwiOlwiQ05cIn0iLCJleHAiOjE3NTQ1NjE1NTh9.oGBjMrsymNK4w3VcokhNqyp-iLfxAbFTmul-468UN6I","device_id": "4e74efec-189b-47d6-b096-7b3529746e67", "new_device_id": "11009","package_name": "com.partyjoy.yoki", "version_code": "17", "language_code": "zh", "lang_country_code": "CN","country_code": "CN", "region": "CN", "device": "Android", "platform": "android", "channel": "google-play","from_page": "com.adealink.weparty.message.conversation.ConversationActivity","req_id": "bbd84549-f460-480f-b328-a2fadf98320f", "app_name": "yoki","Content-Type": "application/json; charset=UTF-8", "Host": "47.83.162.112", "User-Agent": "okhttp/4.12.0"}
    data_list = ast.literal_eval(sys.argv[1])
    request_method = sys.argv[2]
    base = sys.argv[3]
    url = sys.argv[4]
    login_data = json.loads(sys.argv[5].replace("'", '"'))
    header = json.loads(sys.argv[6].replace("'", '"'))
    try:
        start_time = int(datetime.now().timestamp() * 1000)
        coroutines_reuqest(data_list_final=data_list, my_method=request_method, base_domain=base, api_url=url, request_data=login_data,
                         header1=header)
        stop_time = int(datetime.now().timestamp() * 1000)
        print(f'请求耗时: {stop_time - start_time}ms')
    except Exception as e:
        # 捕获并打印运行时的任何异常
        print(f"运行报错: {e}")