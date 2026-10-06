import sys
import os
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout

# 话术库对话框 
class FileItem(QWidget):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setHuaSuDialog = parent
        self.file_path = file_path
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        self.label = QLabel(self.file_path)
        layout.addWidget(self.label)

        self.open_button = QPushButton('编辑')
        self.open_button.clicked.connect(self.open_file)
        layout.addWidget(self.open_button)
        
        self.delete_button = QPushButton('删除')
        self.delete_button.clicked.connect(self.delete_file)
        layout.addWidget(self.delete_button)
        #self.setLayout(layout)
        
    def open_file(self):
        try:
            os.startfile(self.file_path)
        except Exception as e:
            print("打开文件{},出现异常:\n{}".format(self.file_path, e))
            
    def delete_file(self):
        self.setHuaSuDialog.file_paths.remove(self.file_path)
        self.setHuaSuDialog.load_list_item_data()
        return 