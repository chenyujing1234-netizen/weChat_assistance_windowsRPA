import sys
import os
from PyQt5.QtWidgets import QApplication
from dialog_payment import PaymentWindow

if __name__ == '__main__':
    # 确保中文显示正常
    QApplication.setApplicationName("续费充值测试")
    
    app = QApplication(sys.argv)
    dialog = PaymentWindow({})
    
    # 连接信号以测试交互
    def handle_signal(para):
        print(f"收到信号: {para}")
    
    dialog._signal.connect(handle_signal)
    
    # 显示支付窗口
    dialog.show()
    
    sys.exit(app.exec_())