import sys
from PyQt5.QtWidgets import *
from crypt import decrypt, encrypt

# TODO:
# Need to create the code for the user to add to the file
# Create the code for the user creating a password in the GUI if the key doesn't exist

class ReadWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
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
        decrypt()
        with open("log.txt", "r") as keyfile:
            text = keyfile.read()
        encrypt()
        text_edit.setPlainText(text)

        vbox.addWidget(text_edit)
        self.setLayout(vbox)

class AddWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Append...')
        self.setGeometry(0,0,500,500)
        self.off_center()

    def off_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center() * 1.1
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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
    mainWindow = MainWindow()
    sys.exit(app.exec_())