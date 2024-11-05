import requests
import json

# 执行 APi 请求
url = "https://hacker-news.firebaseio.com/v0/item/31353677.json"
r = requests.get(url)
print(f"Status code: {r.status_code}")

# 探索数据结构
response_dict = r.json()
response_string = json.dumps(response_dict, indent=4)
print(response_string)
