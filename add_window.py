import os
import os.path

import dropbox
from cryptography.fernet import Fernet
from PyQt5.Qt import QEvent, Qt
from PyQt5.QtWidgets import (QDesktopWidget, QPushButton, QTextEdit,
                             QVBoxLayout, QWidget)

import access_token
import config


class AddWindow(QWidget):
    # Need to create the window for the user the add to the file
    def __init__(self):
        super().__init__()
        self.appendBox()
        self.initUI()  # Initialise the UI
        # Reads the key and generates the Fernet
        self.f = Fernet(open("key.key", "rb").read())

    def initUI(self):
        self.setWindowTitle('Append...')
        self.setGeometry(0, 0, 500, 500)
        self.off_center()  # Sets the window slightly off from the main window

    def off_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center() * 1.1
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def encrypt(self):
        # Encrypt the file after changes have been made
        with open(config.file_destination, "rb") as log:
            log_data = log.read()
        encrypted_log = self.f.encrypt(log_data)
        with open(config.file_destination, "wb") as log:
            log.write(encrypted_log)

    def decrypt(self):
        # Decrypt the file so changes can be written
        if os.path.isfile(config.file_destination):
            with open(config.file_destination, "rb") as log:
                encrypted_data = log.read()
            if len(encrypted_data) > 0:
                decrypted_data = self.f.decrypt(encrypted_data)
                with open(config.file_destination, "wb") as log:
                    log.write(decrypted_data)

    def appendBox(self):
        layout = QVBoxLayout()

        self.appendData = QTextEdit(self)
        layout.addWidget(self.appendData)
        self.appendData.installEventFilter(self)

        addbtn = QPushButton('Add to Log')
        addbtn.clicked.connect(lambda: self.writeToFile())
        addbtn.setAutoDefault(True)
        layout.addWidget(addbtn)

        self.setLayout(layout)

    def writeToFile(self):
        import time
        date = time.strftime('%d/%m/%Y')
        time = time.strftime('%H:%M:%S')
        self.decrypt()
        with open(config.file_destination, 'a') as myfile:
            myfile.write(
                f"[ {date} - {time} ] - {self.appendData.toPlainText()}\n")
        self.encrypt()
        self.upload()
        self.close()

    def upload(self):
        try:
            # Check if the access token is valid and if it is then upload log.txt to Dropbox
            dbx = dropbox.Dropbox(access_token.access_token)
            with open(config.file_destination, "rb") as logtxt:
                log = logtxt.read()

            dbx.files_upload(
                log, "/log.txt", mode=dropbox.files.WriteMode.overwrite)
        except:
            print("Access token error! Run setup_upload.py to upload to Dropbox")

    # Listens for the user pressing the return/enter key.
    # When return is pressed it executes the writeToFile function
    # This is the same as pressing the "Add to Log" button
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and obj is self.appendData:
            if event.key() == Qt.Key_Return and self.appendData.hasFocus():
                self.writeToFile()
            # elif event.key() == Qt.Key_Escape and self.appendData.hasFocus():
            #     self.close()
        return super().eventFilter(obj, event)

    # Closes the window if the user presses the ESC key
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
