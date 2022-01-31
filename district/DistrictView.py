import sqlite3
import sys
from functools import partial

from PyQt6 import QtWidgets, QtCore


class DistrictView(QtWidgets.QWidget):
    def __init__(self, district_name, parent=None):
        super(DistrictView, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(QtWidgets.QLabel(district_name,self))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dv = DistrictView('Mokotów')
    dv.show()
    app.exec()
