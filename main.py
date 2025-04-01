from dotenv import load_dotenv
import os
import requests

# 加载 .env 文件
load_dotenv()

# 读取配置
api_url = os.getenv("API_URL")
headers = {"Content-Type": "application/json"}

data = {
    "msgtype": "markdown",
    "markdown": {"content": "🙏🙏🇪🇸💪💪"}
}

response = requests.post(api_url, headers=headers, json=data)
print(response.text)
