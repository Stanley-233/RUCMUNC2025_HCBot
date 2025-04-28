from cgitb import enable

from PySide6.QtCore import QDateTime
from dotenv import load_dotenv
import os
import requests

class WechatBot:
    enable = True
    @staticmethod
    def post_md_message(message):
        """
        发送Markdown格式消息到API
        Args:
            message (str): 要发送的Markdown内容
        Returns:
            Response: requests库的响应对象
        """

        if not enable:
            return "已禁用"
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
            print(response.json())
            return response
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None

    @staticmethod
    def post_time_update(sub_phase_type: int, session: int, turn: int, time: QDateTime):
        load_dotenv("ruc.env")
        timeStr = time.toString("yyyy年MM月dd日 hh:mm")
        match sub_phase_type:
            case 0:
                message = (
                    f"## 时间更新\n "
                    f"- 当前会期：第 {session} 会期\n"
                    f"- 当前回合：第 {turn} 个月\n"
                    f"- 会议次元时间：{timeStr}"
                )
            case 1:
                message =  (
                    f"## 时间更新\n "
                    f"- 当前会期：第 {session} 会期\n"
                    f"- 当前回合：第 {turn} 个月\n"
                    f"- 会议次元时间：{timeStr}\n"
                    f"> <font color=\"comment\">注意</font>：现可提交**行动阶段指令**。"
                )
            case 3:
                message =  (
                    f"## 时间更新\n "
                    f"- 当前会期：第 {session} 会期\n"
                    f"- 当前回合：第 {turn} 个月\n"
                    f"- 会议次元时间：{timeStr}\n"
                    f"> <font color=\"comment\">注意</font>：现可提交**支援阶段指令**。"
                )
            case _:
                print(f"错误：阶段类型错误")
                return
        WechatBot.post_md_message(message)

    @staticmethod
    def post_start_time(session: int, ratio: int, time: QDateTime):
        timeStr = time.toString("yyyy年MM月dd日 hh:mm")
        message = (
            f"## 时间轴变动\n"
            f"- 当前会期： {session} \n"
            f"- 会议次元时间：{timeStr}\n"
            f"> <font color=\"comment\">注意</font>：时间轴现已**开启**，当前时间流速 1:{ratio}"
        )
        WechatBot.post_md_message(message)

    @staticmethod
    def post_pause_time(session: int, time: QDateTime):
        timeStr = time.toString("yyyy年MM月dd日 hh:mm")
        message = (
            f"## 时间轴变动\n"
            f"- 当前会期： {session} \n"
            f"- 会议次元时间：{timeStr}\n"
            f"> <font color=\"comment\">注意</font>：时间轴现已**暂停**"
        )
        WechatBot.post_md_message(message)