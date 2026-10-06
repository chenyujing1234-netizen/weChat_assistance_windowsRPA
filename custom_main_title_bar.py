import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy
)
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from log_helper import print_my
from app_info import APP_NAME, APP_IMG_DIR

class CustomMainTitleBar(QWidget):
    _signal = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setStyleSheet("""
            background-color: #1890ff;
            color: white;
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 标题
        self.title = QLabel(APP_NAME)
        self.title.setStyleSheet("padding-left: 10px;")
        self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # 自定义“我的”按钮
        self.btn_my = QPushButton()
        self.btn_my.setFixedSize(50, 50)
        self.btn_my.setIcon(QIcon(f"{APP_IMG_DIR}/me.png")) 
        # 设置图标大小为按钮的一半
        btn_size = self.btn_my.size()
        icon_size = btn_size / 2
        self.btn_my.setIconSize(icon_size)
        self.btn_my.setStyleSheet("border: none; padding: 0px; margin: 0px;")
        self.btn_my.clicked.connect(self.on_my_clicked)

        # 最小化按钮
        self.btn_min = QPushButton("−")
        self.btn_min.setFixedSize(50, 50)
        self.btn_min.setStyleSheet("border: none;")
        self.btn_min.clicked.connect(self.window().showMinimized)

        # 关闭按钮
        self.btn_close = QPushButton("×")
        self.btn_close.setFixedSize(50, 50)
        self.btn_close.setStyleSheet("""
            border: none;
        """)
        self.btn_close.clicked.connect(self.window().close)

        layout.addWidget(self.title)
        layout.addWidget(self.btn_my)
        layout.addWidget(self.btn_min)
        layout.addWidget(self.btn_close)

        self.setLayout(layout)

        # 拖动支持
        self.start = QPoint(0, 0)
        self.pressing = False

    def on_my_clicked(self):
        print("“我的”按钮被点击了！")
        self._signal.emit(f"me_click")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.pos()
            self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.window().move(event.globalPos() - self.start)

    def mouseReleaseEvent(self, event):
        self.pressing = False


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Custom TitleBar Demo")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title_bar = CustomMainTitleBar(self)
        self.title_bar._signal.connect(self.signal_recv_func)
        layout.addWidget(self.title_bar)

        # 主内容区
        content = QLabel("这是主窗口内容区域", self)
        content.setAlignment(Qt.AlignCenter)
        content.setStyleSheet("background-color: #f0f0f0; font-size: 20px;")
        layout.addWidget(content)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())