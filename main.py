import os.path
import sys

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QDialog,
                             QHBoxLayout, QPushButton, QWidget)

import add_window
import read_window
from createKey import CreateKey
from login import Login


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.create_buttons()  # Create the buttons on the UI
        self.initUI()  # Initialise the UI

    def initUI(self):
        self.setWindowTitle('Log')
        self.setGeometry(0, 0, 500, 500)  # Sets the window size to 500x500px
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
        self.readwindow = read_window.ReadWindow()
        self.readwindow.show()

    def open_add_window(self):
        # Same as for read_window
        self.addwindow = add_window.AddWindow()
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
