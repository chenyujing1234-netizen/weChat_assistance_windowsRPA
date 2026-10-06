import sys
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QVBoxLayout, QRadioButton, QPushButton
from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QProcess, QProcessEnvironment
from dialog_add_friend import AddFriendWindow
from dialog_send_circle import SendCircleWindow

class AddTaskWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, add_friend_file_paths, parent):
        super().__init__()
        self.mainWindow = parent
        self.add_friend_file_paths = add_friend_file_paths
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('选择任务类型')
        self.resize(int(350), int(150))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        # 创建垂直布局
        vbox = QVBoxLayout()

        # 创建布局用于放置单选按钮
        hlayout = QVBoxLayout()

        # 创建单选按钮
        self.radio1 = QRadioButton("批量加好友", self)
        self.radio2 = QRadioButton("定时发朋友圈", self)
        # 设置默认选中第一个单选按钮
        self.radio1.setChecked(True)
        self.sel_task_name = "批量加好友"

        # 将单选按钮添加到水平布局中
        hlayout.addWidget(self.radio1)
        hlayout.addWidget(self.radio2)

        self.nextBtn = QPushButton("下一步")
        # 将水平布局和标签添加到垂直布局中
        vbox.addLayout(hlayout)
        vbox.addWidget(self.nextBtn)

        # 设置窗口的布局
        self.setLayout(vbox)

        # 为单选按钮添加点击事件
        self.nextBtn.clicked.connect(self.nextBtnFun)
        self.radio1.clicked.connect(self.radio_clicked)
        self.radio2.clicked.connect(self.radio_clicked)
        
    def radio_clicked(self):
        # 获取选中的单选按钮的文本
        text = self.sender().text()
        print("radio_clicked, 选中的文本是:{}".format(text))
        self.sel_task_name = text
        
    def nextBtnFun(self):
        self.close()
        if self.sel_task_name == "批量加好友":
            self.addFriend_Win = AddFriendWindow(self.add_friend_file_paths)
            self.addFriend_Win._signal.connect(self.mainWindow.signal_recv_func)
            self.addFriend_Win.setWindowModality(Qt.ApplicationModal)
            self.addFriend_Win.show()
            self.addFriend_Win.exec_()
        elif self.sel_task_name == "定时发朋友圈":
            self.sendCircle_Win = SendCircleWindow(self.mainWindow.username_of_can_deposit_list, [], [], self.mainWindow)
            self.sendCircle_Win._signal.connect(self.mainWindow.signal_recv_func)
            self.sendCircle_Win.setWindowModality(Qt.ApplicationModal)
            self.sendCircle_Win.show()
            self.sendCircle_Win.exec_()
        return
        

# 测试
"""
app = QApplication(sys.argv)
dialog = AddTaskWindow()
dialog.show()
sys.exit(app.exec_())
"""