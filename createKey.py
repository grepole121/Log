from PyQt5.QtWidgets import QDialog, \
    QLineEdit, \
    QPushButton, \
    QVBoxLayout, \
    QLabel, \
    QMessageBox
from pass_key_gen import gen_key
import os.path
import config
from cryptography.fernet import Fernet



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
        # If log.txt doesn't exist you can generate a key no matter what
        if not os.path.isfile(config.file_destination):
            gen_key(self.textPass.text(), True)
            # Create empty log.txt file
            open(config.file_destination, 'a').close()
            self.accept()
        else:
            # If log.txt does exist but key.key doesn't this makes sure the key is valid
            with open(config.file_destination, "rb") as log:
                encrypted_data = log.read()
            self.f = Fernet(gen_key(self.textPass.text(), False))
            try:
                # Check if the data can be decrypted with the key
                self.f.decrypt(encrypted_data)
            except:
                # Error if the data cannot be decrypted
                QMessageBox.warning(
                    self, 'Error', 'incorrect password')
            else:
                # If there is no exception raised then generate the key
                gen_key(self.textPass.text(), True)
                self.accept()