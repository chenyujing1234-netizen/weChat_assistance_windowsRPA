import sys
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QVBoxLayout, QRadioButton, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QProcess, QProcessEnvironment
from dialog_add_friend import AddFriendWindow
from dialog_send_circle import SendCircleWindow
from app_info import APP_NAME

class AddDepositObjectWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, parent):
        super().__init__()
        self.mainWindow = parent
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('添加托管对象')
        self.resize(int(350), int(150))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        # 创建垂直布局
        vbox = QVBoxLayout()

        # 创建布局用于放置单选按钮
        hlayout = QVBoxLayout()

        self.label = QLabel("昵称:", self)
        self.userNameEdit = QLineEdit(self)
        hlayout.addWidget(self.label)
        hlayout.addWidget(self.userNameEdit)

        self.confirmBtn = QPushButton("确定")
        self.confirmBtn.clicked.connect(self.confirmBtnFun)
        # 将水平布局和标签添加到垂直布局中
        vbox.addLayout(hlayout)
        vbox.addWidget(self.confirmBtn)

        # 设置窗口的布局
        self.setLayout(vbox)
        
    def confirmBtnFun(self):
        # 获取输入文本
        username = self.userNameEdit.text()
        if len(username) == 0:
            QMessageBox.information(self, APP_NAME, "请输入昵称", QMessageBox.Yes)
            return
            
        self._signal.emit("add_deposit_object_{}".format(username))
        
        self.close()
 
        return
        

# 测试
"""
app = QApplication(sys.argv)
dialog = AddTaskWindow()
dialog.show()
sys.exit(app.exec_())
"""