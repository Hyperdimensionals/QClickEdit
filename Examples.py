import sys

from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QTime

import QClickEdit


class Examples(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.temp = QClickEdit.QSpinBox(23, "Temperature", "C")

        self.ontime = QClickEdit.QTimeEdit(QTime(1, 0, 0, 0), "On Time")
        self.ontime.setDisplayFormat("h:mm:ss ap")

        items = ['asdf', 23, 4, False, list]
        self.boxxx = QClickEdit.QComboBox(items)
        self.boxxx.addItem('aa')
        self.boxxx.setValue('aa')

        self.name = QClickEdit.QLineEdit("Blorka", "Name", "Sr.")

        self.layout.addWidget(self.name)
        self.layout.addWidget(self.temp)
        self.layout.addWidget(self.ontime)
        self.layout.addWidget(self.boxxx)


if __name__ == '__main__':
    from PySide2.QtWidgets import QVBoxLayout

    app = QApplication(sys.argv)

    examples = Examples()
    examples.show()

    # Run main Loop
    sys.exit(app.exec_())
