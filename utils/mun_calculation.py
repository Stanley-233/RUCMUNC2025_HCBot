from PySide6.QtCore import QDateTime

class MunCalculator:
    @staticmethod
    def updateTime(time: QDateTime, elapsed: int, dimension_ratio: int) -> QDateTime:
        # 计算会议次元时间
        total_dimension_seconds = elapsed * dimension_ratio
        # 更新会议次元时间
        return time.addSecs(total_dimension_seconds)
