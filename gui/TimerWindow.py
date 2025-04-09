from utils.Api import Api
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QTextEdit, QPushButton, QHBoxLayout,
                             QStatusBar, QMessageBox)
from PyQt5.QtCore import Qt, QDateTime, QTimer, pyqtSignal


class TimerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api = Api()
        self.init_ui()

    def init_ui(self):
        # 主窗口设置
        self.setWindowTitle('消息发送工具')
        self.setGeometry(300, 300, 500, 400)

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        layout = QVBoxLayout()

        # 时间显示
        self.time_label = QLabel()
        layout.addWidget(self.time_label)

        # 消息输入框
        layout.addWidget(QLabel("请输入消息内容:"))
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("在此输入要发送的消息内容...")
        layout.addWidget(self.message_input)

        # 按钮布局
        button_layout = QHBoxLayout()

        # 发送按钮
        send_btn = QPushButton("发送消息")
        send_btn.clicked.connect(self.send_message)
        button_layout.addWidget(send_btn)

        # 清空按钮
        clear_btn = QPushButton("清空内容")
        clear_btn.clicked.connect(self.clear_input)
        button_layout.addWidget(clear_btn)

        layout.addLayout(button_layout)

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("准备就绪")

        central_widget.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        """更新时间显示"""
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.time_label.setText(f"当前时间: {current_time}")

    def send_message(self):
        """发送消息"""
        message = self.message_input.toPlainText().strip()

        if not message:
            QMessageBox.warning(self, "警告", "消息内容不能为空!")
            return

        self.status_bar.showMessage("正在发送消息...")
        QApplication.processEvents()  # 强制更新UI

        success, result = self.api.send_message(message)

        if success:
            self.status_bar.showMessage("消息发送成功!", 3000)
            QMessageBox.information(self, "成功", "消息已成功发送!")
            self.message_input.clear()
        else:
            self.status_bar.showMessage("消息发送失败", 3000)
            QMessageBox.critical(self, "错误", f"发送失败:\n{result}")

    def clear_input(self):
        """清空输入框"""
        self.message_input.clear()
        self.status_bar.showMessage("内容已清空", 2000)
