# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore    import Qt, QSize
from PyQt5.QtGui     import QPixmap, QPainter, QFont, QFontMetrics, QImage

class PicButton(QPushButton):
    def __init__(self, img_path, text='张三', parent=None):
        super().__init__(parent)
        self._pixmap = QPixmap(img_path)
        self._text   = text
        self.setMinimumSize(100, 100)
        self.setText(self._text)

    # 让布局系统知道按钮的“理想”大小
    def sizeHint(self):
        return self._pixmap.size() + QSize(0, 30)   # 下方留 30px 给文字
    
    # 重写 setText：把文字存起来并刷新
    def setText(self, text):
        self._text = text
        self.update()              # 触发 paintEvent
        
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # 1. 取可绘制区域
        btn_w = self.width()
        btn_h = self.height()

        # 2. 让图片完整显示，保持比例
        pm = self._pixmap.scaled(btn_w, btn_h - 30,   # 留出文字空间
                                 Qt.KeepAspectRatio,
                                 Qt.SmoothTransformation)
        if not self.isEnabled():                       # 禁用变灰
            gray_img = pm.toImage().convertToFormat(QImage.Format_Grayscale8)
            pm = QPixmap.fromImage(gray_img)

        # 3. 居中绘制图片
        px = (btn_w - pm.width())  // 2
        py = 0
        painter.drawPixmap(px, py, pm)

        # 4. 绘制文字
        painter.setPen(Qt.black if self.isEnabled() else Qt.gray)
        font = QFont('Microsoft YaHei', 10, QFont.Bold)
        painter.setFont(font)
        fm  = QFontMetrics(font)
        try:
            tw  = fm.horizontalAdvance(self._text)  # Qt 5.11+
        except AttributeError:
            tw  = fm.width(self._text)  # 旧版 PyQt5 兼容
        th  = fm.height()
        painter.drawText(0, btn_h - th - 8, btn_w, th,
                         Qt.AlignCenter, self._text)


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyQt5 完整显示图片示例')

        self.btn = PicButton('weichat_logo.png', '张三')
        self.btn.clicked.connect(self.toggle_enabled)

        layout = QVBoxLayout(self)
        layout.addWidget(self.btn, alignment=Qt.AlignCenter)

    def toggle_enabled(self):
        self.btn.setEnabled(not self.btn.isEnabled())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.resize(300, 300)
    w.show()
    sys.exit(app.exec_())