import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
                             QMessageBox)
from PyQt5.QtCore import QTimer, QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QColor

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 主窗口设置
        self.setWindowTitle('自动提示消息示例')
        self.setGeometry(200, 200, 400, 300)

        # 创建一个按钮，点击时显示提示
        self.button = QPushButton("显示提示", self)
        self.button.clicked.connect(self.showToolTip)

        # 创建一个提示标签，初始时隐藏
        self.toolTip = QLabel("这是一个提示消息", self)
        self.toolTip.setStyleSheet("background-color: #ffd700; padding: 10px; border-radius: 5px;")
        self.toolTip.setAlignment(Qt.AlignCenter)
        self.toolTip.setFixedSize(200, 50)
        self.toolTip.setWordWrap(True)
        self.toolTip.hide()

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addStretch()
        layout.addWidget(self.toolTip, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        self.show()

    def showToolTip(self):
        # 显示提示
        self.toolTip.show()

        # 创建动画，使提示逐渐显示
        self.animation = QPropertyAnimation(self.toolTip, b"windowOpacity")
        self.animation.setDuration(500)  # 动画持续时间（毫秒）
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

        # 3秒后隐藏提示
        QTimer.singleShot(3000, self.hideToolTip)

    def hideToolTip(self):
        # 创建动画，使提示逐渐消失
        self.animation = QPropertyAnimation(self.toolTip, b"windowOpacity")
        self.animation.setDuration(500)  # 动画持续时间（毫秒）
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

        # 动画结束后隐藏提示
        self.animation.finished.connect(self.toolTip.hide)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())