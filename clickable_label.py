from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel

class ClickableLabel(QLabel):
    # 自定义信号，可带参数也可不带
    clicked = pyqtSignal()

    # 如需区分左右键，可加参数：clicked = pyqtSignal(Qt.MouseButton)
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        # 这里可以判断 event.button() 做左键/右键区分
        self.clicked.emit()          # 发射信号
        super().mousePressEvent(event)