import os
import os.path

from cryptography.fernet import Fernet
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QDesktopWidget, QPlainTextEdit, QVBoxLayout,
                             QWidget)

import config

# The window in which the user can read the contents of the file


class ReadWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()  # Initialise the UI
        # Reads the key and genereates the Fernet
        self.f = Fernet(open("key.key", "rb").read())
        self.readlog()  # Creates the textbox that contains the data and fills it

    def initUI(self):
        self.setWindowTitle('Reading...')
        self.setGeometry(0, 0, 500, 500)
        self.off_center()  # Sets the window slightly off from the main window

    def off_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center() * 1.1
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def readlog(self):
        vbox = QVBoxLayout()

        text_edit = QPlainTextEdit()
        text_edit.setPlainText(self.read_decrypt())
        text_edit.setReadOnly(True)

        vbox.addWidget(text_edit)
        self.setLayout(vbox)

    def read_decrypt(self):
        # Decrypt the file so changes can be written
        if os.path.isfile(config.file_destination):
            with open(config.file_destination, "rb") as log:
                encrypted_data = log.read()
            if len(encrypted_data) > 0:
                decrypted_data = self.f.decrypt(encrypted_data)
                return decrypted_data.decode("utf-8")

    # Closes the window if the user presses the ESC key
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
