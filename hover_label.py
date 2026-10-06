import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QToolTip, QGridLayout
from PyQt5.QtGui import QFont, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QRect

class HoverLabel(QLabel):
    def __init__(self, text, text_tip, parent=None):
        super().__init__(text, parent)
        self.setToolTip(text_tip)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        QToolTip.showText(self.mapToGlobal(self.rect().topRight()), self.toolTip())

    def leaveEvent(self, event):
        QToolTip.hideText()
