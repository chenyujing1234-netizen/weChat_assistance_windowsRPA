import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCalendarWidget, QVBoxLayout, QPushButton, QTableView
from PyQt5.QtCore import QDate, Qt, QRect, QEvent
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont

from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QPen, QBrush, QFont

class CustomCalendarWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.checked_dates = set()  # 存储打勾的日期
        self.setGridVisible(True)  # 显示网格
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)  # 去掉左边的序号列
        
        # 连接 activated 信号到自定义的槽函数
        self.activated.connect(self.on_date_double_clicked)

    def set_checked_date(self, date_str, checked=True):
        try:
            # 将日期字符串解析为 QDate 对象
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            if not date.isValid():
                raise ValueError(f"Invalid date format: {date_str}. Expected format: yyyy-MM-dd")
            if checked:
                self.checked_dates.add(date)
            else:
                self.checked_dates.discard(date)
            self.update()  # 重新绘制整个日历
        except Exception as e:
            print(f"Error: {e}")

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
            new_rect = QRect(rect.x(), rect.y() + 20, rect.width(), rect.height() - 10)  # 偏移 10 像素
            painter.drawText(new_rect, Qt.AlignCenter, "✔")  # 在新的矩形中绘制勾
            painter.restore()



    def on_date_double_clicked(self, date):
        # 打印双击的日期
        print(f"Double-clicked on date: {date.toString('yyyy-MM-dd')}")

# 注意：为了使这段代码运行，你需要有一个完整的 PyQt 应用程序环境。



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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec_())