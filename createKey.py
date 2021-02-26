from PyQt5.QtWidgets import *
from pass_key_gen import gen_key


# This QDialog will open at launch if key.key doesn't exist and the user must create it

class CreateKey(QDialog):
    def __init__(self, parent=None):
        super(CreateKey, self).__init__(parent)
        self.textLabel = QLabel(self)
        self.textLabel.setText("Please create a password: ")
        self.textPass = QLineEdit(self)
        self.textPass.setEchoMode(QLineEdit.Password)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QVBoxLayout(self)
        layout.addWidget(self.textLabel)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        gen_key(self.textPass.text(), True)
        self.accept()