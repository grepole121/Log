from PyQt5.QtWidgets import QDialog, \
    QLineEdit, \
    QPushButton, \
    QVBoxLayout, \
    QMessageBox
from pass_key_gen import gen_key


class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textPass = QLineEdit(self)
        self.textPass.setEchoMode(QLineEdit.Password)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QVBoxLayout(self)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        with open("key.key", 'rb') as keyfile:
            keydata = keyfile.read()
        if keydata == gen_key(self.textPass.text(), False):
            self.accept()
        else:
            QMessageBox.warning(
                self, 'Error', 'incorrect password')