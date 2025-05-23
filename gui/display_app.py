import sys

import toml
from PySide6.QtGui import QFont, QAction
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QLineEdit, QMenuBar
)
from PySide6.QtCore import QTimer, QTime, QDateTime

from utils.mun_calculation import MunCalculator
from utils.wechat_bot import WechatBot

class DisplayApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)

        # Logic
        self.current_session = 1
        self.current_turn = 0
        # 0开始，1行动提交，2行动推演，3支援指令，4支援推演
        self.current_sub_turn = 0
        self.dimension_time = QDateTime(1936,5,9,0,0,0)

        self.window = QWidget()
        self.window.setWindowTitle("RUC时间轴计算广播系统")

        self.layout = QVBoxLayout()
        self.window.setLayout(self.layout)

        # 显示区
        # 设置全局字体
        font = QFont()
        font.setPointSize(14)  # 设置字号为 24
        QApplication.setFont(font)

        # 创建菜单栏
        self.menu_bar = QMenuBar(self.window)

        # 文件菜单
        file_menu = self.menu_bar.addMenu("文件")

        # 保存动作
        save_action = QAction("保存", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # 加载动作
        load_action = QAction("加载", self)
        load_action.triggered.connect(self.load_file)
        file_menu.addAction(load_action)

        self.layout.setMenuBar(self.menu_bar)

        # Label
        self.current_time_label = QLabel("当前时间: ")
        self.meeting_dimension_time_label = QLabel("会议次元时间: " + self.dimension_time.toString("yyyy年MM月dd日 HH:mm:ss"))
        self.current_turn_label = QLabel("当前回合: ")
        self.current_phase_label = QLabel("当前阶段: ")
        self.elapsed_time_label = QLabel("已流逝时间: 0s")

        self.layout.addWidget(self.current_time_label)
        self.layout.addWidget(self.meeting_dimension_time_label)
        self.layout.addWidget(self.current_turn_label)
        self.layout.addWidget(self.current_phase_label)
        self.layout.addWidget(self.elapsed_time_label)

        # 输入与按钮区域
        time_layout = QHBoxLayout()
        self.time_label = QLabel("时间轴比例(1:X):")
        self.time_scale_input = QLineEdit()
        self.time_scale_input.setText("1440")  # 默认值30分钟=1个月
        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.time_scale_input)

        self.layout.addLayout(time_layout)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton("开始时间流动")
        self.pause_button = QPushButton("暂停时间流动")
        self.enable_wechat_button = QPushButton("启用微信广播")
        self.disable_wechat_button = QPushButton("禁用微信广播")
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.enable_wechat_button)
        button_layout.addWidget(self.disable_wechat_button)

        self.layout.addLayout(button_layout)

        # 定时器设置
        self.daemon_timer = QTimer()
        self.daemon_timer.timeout.connect(self.update_current_time)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.start_button.clicked.connect(self.start_time_flow)
        self.pause_button.clicked.connect(self.pause_time_flow)
        self.enable_wechat_button.clicked.connect(self.enable_wechat_button_clicked)
        self.disable_wechat_button.clicked.connect(self.disable_wechat_button_clicked)

        # 初始化时间
        self.elapsed_time = -1
        self.running = False

        self.update_current_time()
        self.window.show()
        self.daemon_timer.start(1000)  # 每秒更新

    def update_current_time(self):
        current_time = QTime.currentTime()
        self.current_time_label.setText(f"当前时间: {current_time.toString()}")

    def update_time(self):
        if self.running:
            self.elapsed_time += 1
            self.elapsed_time_label.setText(f"已流逝时间: {self.elapsed_time}s")
            self.dimension_time = MunCalculator.update_time(self.dimension_time,
                                                            dimension_ratio=int(self.time_scale_input.text()))
            self.meeting_dimension_time_label.setText("会议次元时间: " + self.dimension_time.toString("yyyy年MM月dd日 HH:mm:ss"))
            # 计算阶段与回合
            turn_elapsed_time = self.elapsed_time % (30*60)
            if turn_elapsed_time == 0*60:
                self.current_sub_turn = 0
                self.current_turn += 1
                self.current_turn_label.setText(f"当前回合：{self.current_turn}")
                if self.elapsed_time != 0:
                    WechatBot.post_time_update(self.current_sub_turn, self.current_session, self.current_turn, self.dimension_time)
            elif turn_elapsed_time == 10*60:
                self.current_sub_turn = 1
                WechatBot.post_time_update(self.current_sub_turn, self.current_session, self.current_turn, self.dimension_time)
            elif turn_elapsed_time == 15*60:
                self.current_sub_turn = 2
            elif turn_elapsed_time == 20*60:
                self.current_sub_turn = 3
                WechatBot.post_time_update(self.current_sub_turn, self.current_session, self.current_turn, self.dimension_time)
            elif turn_elapsed_time == 23*60:
                self.current_sub_turn = 4
            match self.current_sub_turn:
                case 0:
                    self.current_phase_label.setText("当前阶段：指令筹备")
                case 1:
                    self.current_phase_label.setText("当前阶段：行动指令窗口")
                case 2:
                    self.current_phase_label.setText("当前阶段：行动结束")
                case 3:
                    self.current_phase_label.setText("当前阶段：支援指令窗口")
                case 4:
                    self.current_phase_label.setText("当前阶段：支援结束")

    def start_time_flow(self):
        if not self.running:
            self.running = True
            self.timer.start(1000)  # 每秒更新
            WechatBot.post_start_time(self.current_session, int(self.time_scale_input.text()), self.dimension_time)

    def pause_time_flow(self):
        if self.running:
            self.running = False
            self.timer.stop()
            WechatBot.post_pause_time(self.current_session, self.dimension_time)

    def save_file(self):
        config_data = {
            "session": self.current_session,
            "turn": self.current_turn,
            "sub_turn": self.current_sub_turn,
            "dimension_time": self.dimension_time.toString("yyyy-MM-dd HH:mm:ss")
        }
        with open("config.toml", "w") as config_file:
            toml.dump(config_data, config_file)
        print("配置已保存到 config.toml")

    def load_file(self):
        try:
            with open("config.toml", "r") as config_file:
                config_data = toml.load(config_file)
                self.current_session = config_data["session"]
                self.current_turn = config_data["turn"]
                self.current_sub_turn = config_data["sub_turn"]
                self.dimension_time = QDateTime.fromString(config_data["dimension_time"], "yyyy-MM-dd HH:mm:ss")
                print("配置已加载")
        except FileNotFoundError:
            print("配置文件未找到")
        except Exception as e:
            print(f"加载配置时出错: {e}")

    @staticmethod
    def enable_wechat_button_clicked():
        WechatBot.enable = True

    @staticmethod
    def disable_wechat_button_clicked():
        WechatBot.enable = False
