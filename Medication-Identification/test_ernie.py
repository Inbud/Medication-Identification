# 临时测试脚本 ernie_test.py
import erniebot
from config import ERNIE_ACCESS_TOKEN

erniebot.api_type = 'aistudio'
erniebot.access_token = ERNIE_ACCESS_TOKEN

try:
    response = erniebot.ChatCompletion.create(
        model='ernie-4.0',
        messages=[{'role': 'user', 'content': '你好'}]
    )
    print("测试成功，响应:", response.get_result())
except Exception as e:
    print("测试失败:", e)