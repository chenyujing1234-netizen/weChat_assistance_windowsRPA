from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QFontMetrics, QPixmap, QPainter
from PyQt5.QtWidgets import QTabBar, QStyleOptionTab, QStyle
from app_info import g_desktop_w

class CustomTabBar(QTabBar):
    def __init__(self, b_need_text_bold = False, parent=None):
        super().__init__(parent)
        self._icons = {}          # index -> QPixmap

        # 字号放大 3pt
        f = self.font()
        f.setPointSize(f.pointSize() + 3)
        self.setFont(f)
        self._b_need_text_bold = b_need_text_bold

    # ----------------- 外部设置图标 -----------------
    def setTabIcon(self, index, png_path, png_path_disable):
        self._icons[index] = {}
        self._icons[index]["pm_enable"] = QPixmap(png_path).scaled(
            24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._icons[index]["pm_disable"] = QPixmap(png_path_disable).scaled(
            24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.update()

    # ----------------- 宽度：刚好容纳内容 -----------------
    def tabSizeHint(self, index):
        fm = QFontMetrics(self.font())
        text_w = fm.width(self.tabText(index))
        icon_w = 24 if index in self._icons else 0
        # 总宽度 = 图标(24) + 图标右侧间隙(6) + 文本 + 左右留白(8*2)
        #w = 8 + icon_w + 6 + text_w + 8
        w = 8 + icon_w + 6 + text_w + 8 + 8
        h = fm.height() + 16
        return QSize(w, h)

    # ----------------- 绘制 -----------------
    def paintEvent(self, event):
        painter = QPainter(self)
        for i in range(self.count()):
            opt = QStyleOptionTab()
            self.initStyleOption(opt, i)

            # 1. 形状
            self.style().drawControl(QStyle.CE_TabBarTabShape, opt, painter, self)

            # 2. 图标
            icon_width = 0
            if i in self._icons:
                if i == self.currentIndex():
                    pm = self._icons[i]["pm_enable"]
                else:
                    pm = self._icons[i]["pm_disable"]
                icon_rect = opt.rect.adjusted(8, 0, 0, 0)
                icon_rect.setSize(pm.size())
                icon_rect.moveTop(opt.rect.center().y() - pm.height() // 2)
                painter.drawPixmap(icon_rect, pm)
                icon_width = pm.width() + 6

            # 3. 文字（颜色 + 位置）
            text_rect = opt.rect.adjusted(icon_width + 14, 0, -8, 0)
            painter.setPen(Qt.blue if i == self.currentIndex() else Qt.black)
            
            # 设置粗体字体
            font = painter.font()
            font.setBold(self._b_need_text_bold)
            painter.setFont(font)
            
            painter.drawText(text_rect,
                             Qt.AlignLeft | Qt.AlignVCenter,
                             self.tabText(i))

"""
# 自定义的TabBar
class CustomTabBar(QTabBar):        
    def tabSizeHint(self, index):
        width = int(g_desktop_w/13)
        #width = int(g_desktop_w/18)
        # 获取系统默认的大小
        size = super().tabSizeHint(index)
        # 获取当前标签页的文本
        text = self.tabText(index)
        #print(f"CustomTabBar, text：{text}")
        # 计算文本宽度
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(text)
        text_width = int(text_width/62*width)
        #print(f"CustomTabBar, text_width:{text_width}")
        # 设置宽度为文本宽度加上一些额外空间
        size.setWidth(text_width)
        return size
    
    def paintEvent(self, event):
        painter = QPainter(self)
        for i in range(self.count()):
            option = QStyleOptionTab()
            self.initStyleOption(option, i)
            # 使用正确的属性名
            self.style().drawControl(QStyle.CE_TabBarTabShape, option, painter, self)
            self.style().drawControl(QStyle.CE_TabBarTabLabel, option, painter, self)
"""