import sys
import os
import os.path
from pass_key_gen import gen_key
from PyQt5.QtWidgets import *
# from crypt import decrypt, encrypt
from login import Login
from createKey import CreateKey
from cryptography.fernet import Fernet

# Current state of program:
# First time opening user will be prompted to create a password
# After that user will be prompted to enter the password and if it matches the key program will open
# User can read the contents of the file after logging in
# User can not yet append to the file


# TODO:
# Need to create the code for the user to add to the file.
# If the key is deleted and then recreated with the wrong password must not allow key to be made and return error.

file_destination = "/home/george/MEGA/Log/New/log.txt"

class ReadWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.f = Fernet(open("key.key", "rb").read())
        self.readlog()

    def initUI(self):
        self.setWindowTitle('Reading...')
        self.setGeometry(0,0,500,500)
        self.off_center()

    def off_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center() * 1.1
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def readlog(self):
        vbox = QVBoxLayout()

        text_edit = QPlainTextEdit()
        self.decrypt()
        with open("log.txt", "r") as keyfile:
            text = keyfile.read()
        self.encrypt()
        text_edit.setPlainText(text)

        vbox.addWidget(text_edit)
        self.setLayout(vbox)

    def encrypt(self):
        #Encrypt the file after changes have been made
        with open(file_destination, "rb") as log:
            log_data = log.read()
        encrypted_log = self.f.encrypt(log_data)
        with open(file_destination, "wb") as log:
            log.write(encrypted_log)

    def decrypt(self):
        #Decrypt the file so changes can be written
        if os.path.isfile(file_destination):
            with open(file_destination, "rb") as log:
                encrypted_data = log.read()
            decrypted_data = self.f.decrypt(encrypted_data)
            with open(file_destination, "wb") as log:
                log.write(decrypted_data)

class AddWindow(QWidget):
    # Need to create the window for the user the add to the file
    def __init__(self):
        super().__init__()
        self.initUI()
        self.f = Fernet(open("key.key", "rb").read())

    def initUI(self):
        self.setWindowTitle('Append...')
        self.setGeometry(0,0,500,500)
        self.off_center()

    def off_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center() * 1.1
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def encrypt(self):
        #Encrypt the file after changes have been made
        with open(file_destination, "rb") as log:
            log_data = log.read()
        encrypted_log = self.f.encrypt(log_data)
        with open(file_destination, "wb") as log:
            log.write(encrypted_log)

    def decrypt(self):
        #Decrypt the file so changes can be written
        if os.path.isfile(file_destination):
            with open(file_destination, "rb") as log:
                encrypted_data = log.read()
            decrypted_data = self.f.decrypt(encrypted_data)
            with open(file_destination, "wb") as log:
                log.write(decrypted_data)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.readwindow = ReadWindow()
        self.addwindow  = AddWindow()
        self.create_buttons()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Log')
        self.setGeometry(0,0,500,500)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_read_window(self):
        self.readwindow.show()

    def create_buttons(self):
        layout = QHBoxLayout()

        readbtn = QPushButton('Read')
        readbtn.clicked.connect(lambda: self.open_read_window())
        layout.addWidget(readbtn)

        addbtn = QPushButton('Add to Log')
        addbtn.clicked.connect(lambda: self.open_add_window())
        layout.addWidget(addbtn)

        self.setLayout(layout)

    def open_add_window(self):
        self.addwindow.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    if os.path.isfile('key.key'):
        login = Login()
        if login.exec_() == QDialog.Accepted:
            mainWindow = MainWindow()
            sys.exit(app.exec_())
    else:
        createKey = CreateKey()
        if createKey.exec_() == QDialog.Accepted:
            mainWindow = MainWindow()
            sys.exit(app.exec_())

