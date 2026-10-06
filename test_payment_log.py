import sys
from PyQt5.QtWidgets import QApplication
from dialog_payment import PaymentWindow

if __name__ == '__main__':
    # 确保中文显示正常
    QApplication.setApplicationName("续费充值测试")
    
    app = QApplication(sys.argv)
    # 创建一个模拟的配置数据对象用于测试
    mock_config = {
        "BIND_PHONE": "15280006511",
        "USERNAME": "测试用户"
    }
    
    dialog = PaymentWindow(mock_config)
    dialog.show()
    sys.exit(app.exec_())