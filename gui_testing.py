import sys

# 1. Import `QApplication` and all the required widgets
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('PyQt5 App')
window.setGeometry(100, 100, 600, 600)
window.move(60, 15)
helloMsg = QLabel('<h1>Hello World!</h1>', parent=window)
helloMsg.move(60, 15)

vbox = QVBoxLayout()

text_edit = QPlainTextEdit()
text=open('log.txt').read()
text_edit.setPlainText(text)

vbox.addWidget(text_edit)
window.setLayout(vbox)


window.show()
sys.exit(app.exec_())
