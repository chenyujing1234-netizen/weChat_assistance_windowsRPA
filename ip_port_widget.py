from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QMessageBox
import ipaddress


class IpPortWidget(QWidget):
    valid_changed = pyqtSignal(bool)   # 输入合法/非法时发射 True/False

    def __init__(self,
                 parent=None,
                 default_ip='127.0.0.1',
                 default_port="8000",
                 label_text='地址:'):
        super().__init__(parent)

        # --- 控件 ---
        self.label = QLabel(label_text)

        self.ip_edit = QLineEdit(default_ip)
        self.ip_edit.setInputMask('000.000.000.000;_')
        self.ip_edit.setFixedWidth(160)
        self.ip_edit.textChanged.connect(self._check)

        self.port_edit = QLineEdit(str(default_port))
        self.port_edit.setFixedWidth(70)
        self.port_edit.setValidator(QIntValidator(1, 65535, self))
        self.port_edit.textChanged.connect(self._check)

        # --- 布局 ---
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        layout.addWidget(self.ip_edit)
        layout.addWidget(QLabel('端口:'))
        layout.addWidget(self.port_edit)
        layout.addStretch()

        self._check()     # 初始化校验

    # --------------------------------------------------
    # 对外接口：自动校验 + 弹窗提示
    # --------------------------------------------------
    def address(self):
        """
        获取合法 (ip, port)；若非法则弹窗提示并返回 (None, None)
        """
        ip_txt = self.ip_edit.text().strip()
        port_txt = self.port_edit.text().strip()

        # 1. 空值检查
        if not ip_txt or not port_txt:
            QMessageBox.warning(self, "输入不完整", "IP 地址和端口号不能为空！")
            return None, None

        # 2. IP 格式检查
        try:
            ip = str(ipaddress.ip_address(ip_txt))
        except ValueError:
            QMessageBox.warning(self, "IP 地址不合法", f"“{ip_txt}” 不是一个有效的 IP 地址。")
            return None, None

        # 3. 端口范围检查
        try:
            port = int(port_txt)
            if not (0 < port < 65536):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "端口号不合法", "端口号必须是 1-65535 之间的整数。")
            return None, None

        return ip, str(port)

    # --------------------------------------------------
    def set_address(self, ip, port):
        """外部设置 IP 与端口"""
        self.ip_edit.setText(str(ip))
        self.port_edit.setText(str(port))

    # --------------------------------------------------
    def _check(self):
        """内部：仅发射 valid_changed，不弹窗"""
        ip, port = self._raw_address()
        self.valid_changed.emit(ip is not None and port is not None)

    def _raw_address(self):
        """返回 (ip, port) 或 (None, None)，不弹窗"""
        try:
            ip = str(ipaddress.ip_address(self.ip_edit.text().strip()))
            port = int(self.port_edit.text())
            if not (0 < port < 65536):
                raise ValueError
            return ip, port
        except ValueError:
            return None, None
        
        
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP + 端口控件演示")

        self.ip_port = IpPortWidget(self, default_ip='192.168.1.1', default_port="22")
        self.ip_port.valid_changed.connect(self.on_validity_changed)

        self.btn = QPushButton("获取地址")
        self.btn.clicked.connect(self.show_address)

        layout = QVBoxLayout(self)
        layout.addWidget(self.ip_port)
        layout.addWidget(self.btn)

    def on_validity_changed(self, ok):
        self.btn.setEnabled(ok)

    def show_address(self):
        ip, port = self.ip_port.address()
        print(f"当前地址：{ip}:{port}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    sys.exit(app.exec_())