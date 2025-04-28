from PySide6.QtCore import QDateTime

class MunCalculator:
    @staticmethod
    def update_time(time: QDateTime, dimension_ratio: int) -> QDateTime:
        return time.addSecs(dimension_ratio)
