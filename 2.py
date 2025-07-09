import re, json, requests

login_data = {
    "content": "{\"emotionId\":34}",
    "fromUid":100047493, #100044752
    "isIncludeSender": 1,
    "messageType": "app:emotion",
    "target": "#man#" #100046401
}
my_header = {
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
data_need_replace = len(re.findall(r'#.*?#', json.dumps(login_data)))
header_need_replace = len(re.findall(r'#.*?#', json.dumps(my_header)))

if data_need_replace > 0 and header_need_replace == 0:
    print(1)
elif data_need_replace == 0 and header_need_replace > 0:
    print(2)
elif data_need_replace == 0 and header_need_replace == 0:
    print(3)
else:
    print(4)


new_data = {
    "accessToken": "",
    "lang": "zh",
    "appsflyerId": "1746774807412-2336603580584834356",
    "channel": "google-play",
    "country": "",
    "deviceId": "0e7d3a24-1460-4bd7-b58a-10311e1cde5a",
    "deviceToken": "v2:txoG3OpRgFH7U82bfmiihp6eYzDmiwwSUa7zeKrsQEZ6jHeKxrua/T24ZxqV0rzujRxjf75dc1ye0BTSJS5CgY1kpEHTbJADCIJ8Y8LEpL1Ousi2HVnGsp9srcR1VzsmEUSouo04w0RF/m8yE6ubbixHR1VXp66TtF8N0bjoXUP4Ajge8rUDGTZf0BHQ3vpLKrGhwUZUKQxi2tEOhdUynJCD5VsdEC21Kfvf2awSWQB8v3z2tLuWwXNR34yxa/GsWVbDBJR4oH/dRrNl1EPOfhDmqEc6ilmC7Cio7Cf+GgTX9HtRguxo",
    "fbAccount": "981231",
    "newDeviceId": "11126",
    "packageName": "com.partyjoy.yoki",
    "platform": "android",
    "seqid": 0,
    "simMcc": "",
    "fromSimulator": False,
    "systemLang": "zh",
    "thirdType": "fb",
    "versionCode": 9,
    "virtualApk": False
}

response = requests.post(url='http://47.83.162.112/api/account/login', json=login_data, headers=None)


print(response.json())




