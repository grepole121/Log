from PyQt5.QtWidgets import *
import sys
from pass_key_gen import gen_key

class Append(QDialog):
    def __init__(self, parent=None):
        super(Append, self).__init__(parent)
        self.gettext()

    def gettext(self):
        text, ok = QInputDialog.getText(self, 'Append to the file', 'Type below:')

        if ok:
            self.le1.setText(str(text))

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.appendWindow()
        self.initUI()
        self.center()


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

    # def appendWindow(self):
    #     appendData = QTextEdit(self)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())