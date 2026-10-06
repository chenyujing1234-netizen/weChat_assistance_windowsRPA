import sys
from PyQt5.QtWidgets import QApplication, QTableView, QAbstractItemView, QStyledItemDelegate, QWidget, QVBoxLayout, QHeaderView, QPushButton
from PyQt5.QtGui import QIcon, QFont, QColor, QTextCursor, QStandardItemModel, QStandardItem
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt

class ButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        # 绘制按钮的矩形区域
        rect = option.rect
        # 绘制一个按钮
        painter.save()
        painter.setRenderHint(painter.Antialiasing)
        painter.setBrush(QBrush(QColor(200, 200, 200)))
        painter.drawRoundedRect(rect, 5, 5)
        painter.restore()

        # 绘制文本
        super().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        # 创建一个按钮作为编辑器
        button = QPushButton('删除', parent)
        button.clicked.connect(lambda: print("Button clicked"))
        return button

    def setEditorData(self, editor, index):
        # 设置编辑器数据
        pass

    def setModelData(self, editor, model, index):
        # 设置模型数据
        pass

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建模型
        self.model = QStandardItemModel(3, 4)  # 3行4列

        # 创建视图
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setItemDelegate(ButtonDelegate(self))  # 设置自定义委托

        # 将按钮项添加到模型的特定位置
        self.model.setItem(1, 1, QStandardItem('Button'))  # 将按钮占位符放在第2行第2列

        # 设置列宽和行高
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        # 显示窗口
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())