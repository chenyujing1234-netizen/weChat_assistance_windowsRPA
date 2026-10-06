import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

import sys
from PyQt5.QtWidgets import QApplication, QTableView, QAbstractItemView, QStyledItemDelegate, QWidget, QVBoxLayout, QHeaderView, QPushButton
from PyQt5.QtGui import QIcon, QFont, QColor, QTextCursor, QStandardItemModel, QStandardItem
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt


class ButtonItem(QStandardItem):
    def __init__(self, text):
        super().__init__()
        self.button = QPushButton(text)
        self.button.clicked.connect(self.on_button_clicked)
        self.setEditable(False)  # 按钮项不可编辑

    def on_button_clicked(self):
        print("Button clicked")

    def widget(self):
        return self.button

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model = QStandardItemModel(3, 4)  # 3行4列
        self.model.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3', 'Column 4'])

        # 在(1,1)位置添加按钮
        self.add_button(1, 1, "Click Me")

        # 创建视图
        self.view = self.create_view()
        self.setCentralWidget(self.view)

    def create_view(self):
        view = QTableView(self)
        view.setModel(self.model)
        return view

    def add_button(self, row, column, text):
        # 创建一个ButtonItem，并设置按钮文本
        button_item = ButtonItem(text)
        # 将ButtonItem添加到模型中
        self.model.setItem(row, column, button_item)

# 创建应用程序
app = QApplication(sys.argv)

# 创建主窗口
main_window = MainWindow()
main_window.show()

# 运行应用程序
sys.exit(app.exec_())