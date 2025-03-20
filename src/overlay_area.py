from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect

class OverlayCaptureArea(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(200, 200, 600, 400)

    def get_area(self):
        """キャプチャ範囲を返す"""
        geometry: QRect = self.geometry()
        return geometry.x(), geometry.y(), geometry.width(), geometry.height()
