from dotenv import load_dotenv
import os
import requests
import json

class Api:  # 类名建议使用大写开头的驼峰命名
    def __init__(self):
        load_dotenv("ruc.env")
        self.api_url = os.getenv("API_URL")  # 保存为实例变量
        self.headers = {"Content-Type": "application/json"}  # 保存为实例变量

    @staticmethod
    def post_md_message(message):
        """
        发送Markdown格式消息到API
        Args:
            message (str): 要发送的Markdown内容
        Returns:
            Response: requests库的响应对象
        """
        # 创建API实例获取配置
        api_instance = Api()

        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": message
            }
        }

        try:
            response = requests.post(
                url=api_instance.api_url,
                headers=api_instance.headers,
                json=data  # 直接使用json参数会自动序列化并设置Content-Type
            )
            response.raise_for_status()  # 如果响应状态码不是200，抛出异常
            return response
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None
