# 使用方法
from utils.Api import Api
from datetime import datetime

current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
message = f"⏰ 当前时间: {current_time}"
result = Api.post_md_message(message)
if result:
    print(f"发送成功，状态码: {result.status_code}")
    print(f"响应内容: {result.text}")
