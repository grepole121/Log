import sys

# 1. Import `QApplication` and all the required widgets
from PyQt5.QtWidgets import *
from crypt import encrypt, decrypt


app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('PyQt5 App')
window.setGeometry(100, 100, 600, 600)
window.move(60, 15)


vbox = QVBoxLayout()

text_edit = QPlainTextEdit()
# decrypt()
with open("log.txt", "r") as keyfile:
    text = keyfile.read()
# encrypt()
text_edit.setPlainText(text)

vbox.addWidget(text_edit)
window.setLayout(vbox)


window.show()
sys.exit(app.exec_())
