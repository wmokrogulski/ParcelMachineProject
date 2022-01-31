import sys

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import QObject

from CityView import CityView
from district.DistrictView import DistrictView


class CustomerMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(CustomerMainWindow, self).__init__()
        self.setObjectName('CustomerMainWindow')
        self.setWindowTitle("Aplikacja do zarządzania paczkomatami")
        self.setMinimumSize(600, 400)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        self.setCityView()

    def setDistrictView(self, district_name):
        dv = DistrictView(district_name)
        self.setCentralWidget(dv)

    def setCityView(self):
        cv = CityView(self)
        self.setCentralWidget(cv)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    cmw = CustomerMainWindow()
    cmw.show()
    app.exec()
