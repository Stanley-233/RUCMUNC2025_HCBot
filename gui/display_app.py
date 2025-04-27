import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QSpinBox,
    QPushButton,
    QHBoxLayout, QLineEdit,
)
from PySide6.QtCore import QTimer, QTime, QDateTime
from utils.mun_calculation import MunCalculator

class DisplayApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.window = QWidget()
        self.window.setWindowTitle("RUC时间轴计算广播系统")

        self.layout = QVBoxLayout()
        self.window.setLayout(self.layout)

        self.dimension_time = QDateTime(1936,5,9,0,0,0)

        # 显示区
        self.current_time_label = QLabel("当前时间: ")
        self.meeting_dimension_time_label = QLabel("会议次元时间: " + self.dimension_time.toString("yyyy年MM月dd日 HH:mm:ss"))
        self.current_round_label = QLabel("当前回合: ")
        self.current_phase_label = QLabel("当前阶段: ")
        self.elapsed_time_label = QLabel("已流逝时间: 0s")

        self.layout.addWidget(self.current_time_label)
        self.layout.addWidget(self.meeting_dimension_time_label)
        self.layout.addWidget(self.current_round_label)
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
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)

        self.layout.addLayout(button_layout)

        # 定时器设置
        self.deamonTimer = QTimer()
        self.deamonTimer.timeout.connect(self.update_current_time)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.start_button.clicked.connect(self.start_time_flow)
        self.pause_button.clicked.connect(self.pause_time_flow)

        # 初始化时间
        self.elapsed_time = 0
        self.running = False

        self.update_current_time()
        self.window.show()
        self.deamonTimer.start(1000)  # 每秒更新

    def update_current_time(self):
        current_time = QTime.currentTime()
        self.current_time_label.setText(f"当前时间: {current_time.toString()}")

    def update_time(self):
        if self.running:
            self.elapsed_time += 1
            self.elapsed_time_label.setText(f"已流逝时间: {self.elapsed_time}s")
            self.dimension_time = MunCalculator.updateTime(self.dimension_time,
                                                           elapsed=self.elapsed_time,
                                                           dimension_ratio=int(self.time_scale_input.text()))
            self.meeting_dimension_time_label.setText("会议次元时间: " + self.dimension_time.toString("yyyy年MM月dd日 HH:mm:ss"))

    def start_time_flow(self):
        if not self.running:
            self.running = True
            self.timer.start(1000)  # 每秒更新

    def pause_time_flow(self):
        if self.running:
            self.running = False
            self.timer.stop()

    @staticmethod
    def closeAllWindows():
        super().closeAllWindows()
        sys.exit(0)

if __name__ == "__main__":
    app = DisplayApp()
    sys.exit(app.exec())