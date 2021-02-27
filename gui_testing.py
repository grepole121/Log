import sys
import os
import os.path
from PyQt5.QtWidgets import *
from PyQt5.Qt import QEvent
from PyQt5.Qt import Qt
from login import Login
from createKey import CreateKey
from cryptography.fernet import Fernet



# Current state of program:
# First time opening user will be prompted to create a password
# After that user will be prompted to enter the password and if it matches the key program will open
# User can read the contents of the file after logging in
# User can now append to the file. Can press enter instead of needing to click the button
# Escape key will now close the current window in focus


# TODO:
# If the key is deleted and then recreated with the wrong password must not allow key to be made and return error.


# Destination the log is saved in
file_destination = "/home/george/MEGA/Log/New/log.txt"

# The window in which the user can read the contents of the file
class ReadWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() # Initialise the UI
        self.f = Fernet(open("key.key", "rb").read()) # Reads the key and genereates the Fernet
        self.readlog() # Creates the textbox that contains the data and fills it

    def initUI(self):
        self.setWindowTitle('Reading...')
        self.setGeometry(0,0,500,500)
        self.off_center() # Sets the window slightly off from the main window

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
        text_edit.setReadOnly(True)

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

    # Closes the window if the user presses the ESC key
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

class AddWindow(QWidget):
    # Need to create the window for the user the add to the file
    def __init__(self):
        super().__init__()
        self.appendBox()
        self.initUI() # Initialise the UI
        self.f = Fernet(open("key.key", "rb").read()) # Reads the key and genereates the Fernet

    def initUI(self):
        self.setWindowTitle('Append...')
        self.setGeometry(0,0,500,500)
        self.off_center() # Sets the window slightly off from the main window

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
        with open("/home/george/MEGA/Log/New/log.txt", 'a') as myfile:
            myfile.write('[ ' + date + ' - ' + time + ' ] - ' + self.appendData.toPlainText() + '\n')
        self.encrypt()
        self.close()

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


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.create_buttons() # Create the buttons on the UI
        self.initUI() # Initialise the UI

    def initUI(self):
        self.setWindowTitle('Log')
        self.setGeometry(0,0,500,500) # Sets the window size to 500x500px
        self.center()
        self.show()

    # Centers the window
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_read_window(self):
        # Opens generates an instance of the read window
        # Shows the read window
        # It generates a new instance everytime to refresh the data in case it has been updated
        self.readwindow = ReadWindow()
        self.readwindow.show()

    def open_add_window(self):
        # Same as for read_window
        self.addwindow = AddWindow()
        self.addwindow.show()

    def create_buttons(self):
        layout = QHBoxLayout()
        # Creates a horizontal layout

        # Creates the read button and runs the open_read_window function when clicked
        readbtn = QPushButton('Read')
        readbtn.clicked.connect(lambda: self.open_read_window())
        layout.addWidget(readbtn)

        # Same as read button but for add
        addbtn = QPushButton('Add to Log')
        addbtn.clicked.connect(lambda: self.open_add_window())
        layout.addWidget(addbtn)

        # Sets the layout
        self.setLayout(layout)

    # Closes the window if the user presses the ESC key
    # Opens read window if user presses 'r'
    # Opens add window if user presses 'a'
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_R:
            self.open_read_window()
        elif event.key() == Qt.Key_A:
            self.open_add_window()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Checks if the key exists
    # If key exists run the login code
    # If key doesn't exist run the code for the user to create the key
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

