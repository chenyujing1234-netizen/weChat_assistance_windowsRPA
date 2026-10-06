import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCalendarWidget, QVBoxLayout, QPushButton, QTableView
from PyQt5.QtCore import QDate, Qt, QRect, QEvent, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont

# 自定义日历
class CustomCalendarWidget(QCalendarWidget):
    _signal = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.checked_dates = set()  # 存储打勾的日期
        self.setGridVisible(True)  # 显示网格
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)  # 去掉左边的序号列
        
        self.activated.connect(self.on_date_double_clicked)

    def set_checked_date(self, date_str, checked=True):
        """设置指定日期的打勾状态，日期以字符串形式传入，如 '2024-07-12'"""
        try:
            # 将日期字符串解析为 QDate 对象
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            if not date.isValid():
                raise ValueError(f"Invalid date format: {date_str}. Expected format: yyyy-MM-dd")
        except Exception as e:
            print(f"Error: {e}")
            return

        if checked:
            self.checked_dates.add(date)
        else:
            self.checked_dates.discard(date)
        self.updateCell(date)  # 更新单元格显示

    def clear_checked_dates(self):
        """清除所有打勾的状态"""
        self.checked_dates.clear()  # 清空打勾日期集合
        self.update()  # 重新绘制整个日历

    def paintCell(self, painter, rect, date):
        """重写绘制单元格的方法"""
        super().paintCell(painter, rect, date)  # 调用父类的绘制方法

        # 如果当前日期在打勾日期集合中，绘制一个勾
        if date in self.checked_dates:
            painter.save()
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.setBrush(QBrush(Qt.NoBrush))
            painter.setFont(QFont("Arial", 22, QFont.Bold))
            
            # 创建一个新的 QRect，将原矩形的 y 值向下偏移
            new_rect = QRect(rect.x() + 10, rect.y() + 20, rect.width(), rect.height() - 10)  # 偏移 10 像素
            painter.drawText(new_rect, Qt.AlignCenter, "✔")  # 在新的矩形中绘制勾
            painter.restore()
            
    def on_date_double_clicked(self, date):
        date_str = date.toString('yyyy-MM-dd')
        print(f"双击是日期: {date_str}")
        self._signal.emit("double_clicked_{}".format(date_str))
        
class CalendarApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        print('sdfdddddddddd')
        self.setWindowTitle("Custom Calendar")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout(self)

        self.calendar = CustomCalendarWidget(self)
        layout.addWidget(self.calendar)

        # 添加一个按钮用于清除所有打勾状态
        clear_button = QPushButton("清除所有打勾状态", self)
        clear_button.clicked.connect(self.calendar.clear_checked_dates)
        layout.addWidget(clear_button)

        # 示例：设置某些日期为打勾状态
        self.calendar.set_checked_date("2025-03-05")
        self.calendar.set_checked_date("2025-03-10")
        self.calendar.set_checked_date("2025-03-15", checked=False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec_())