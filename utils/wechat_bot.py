from PySide6.QtCore import QDateTime
from dotenv import load_dotenv
import os
import requests

class WechatBot:
    @staticmethod
    def post_md_message(message):
        """
        发送Markdown格式消息到API
        Args:
            message (str): 要发送的Markdown内容
        Returns:
            Response: requests库的响应对象
        """
        load_dotenv("ruc.env")

        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": message
            }
        }

        try:
            response = requests.post(
                url=os.getenv("API_URL"),
                headers={"Content-Type": "application/json"},
                json=data  # 直接使用json参数会自动序列化并设置Content-Type
            )
            response.raise_for_status()  # 如果响应状态码不是200，抛出异常
            return response
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None

    @staticmethod
    def post_time_update(sub_phase_type: int, session: int, turn: int, time: QDateTime):
        load_dotenv("ruc.env")
        timeStr = time.toString("yyyy年MM月dd日")
        message = ""
        match sub_phase_type:
            case 0:
                message = f"时间更新信息：\n "
                f"- 当前会期：第 {session} 会期"
                f"- 当前回合：第 {turn} 个月"
                f"- 当前时间：{timeStr}"
            case 1:
                message =  f"时间更新信息：\n "
                f"- 当前会期：第 {session} 会期"
                f"- 当前回合：第 {turn} 个月"
                f"- 当前时间：{timeStr}"
                f"> <font color=\"comment\">注意</font>：现可提交**行动阶段指令**。"
            case 3:
                message =  f"时间更新信息：\n "
                f"- 当前会期：第 {session} 会期"
                f"- 当前回合：第 {turn} 个月"
                f"- 当前时间：{timeStr}"
                f"> <font color=\"comment\">注意</font>：现可提交**支援阶段指令**。"
            case _:
                print(f"错误：阶段类型错误")
        WechatBot.post_md_message(message)
