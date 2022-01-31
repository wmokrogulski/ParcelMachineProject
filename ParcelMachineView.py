import sqlite3
import sys
from enum import Enum
from functools import partial

from PyQt6 import QtWidgets, QtGui, QtCore

from parcel_machine import ParcelMachine, ParcelTank
from parcel_machine.Ui_ParcelMachine import Ui_Form


class ParcelMachineView(QtWidgets.QWidget, Ui_Form):
    class ActionType(Enum):
        RECEIVE = 1
        SEND = 2

    # class ParcelMachineView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ParcelMachineView, self).__init__(parent)
        self.setupUi(self)
        self.pm = ParcelMachine(1)
        # self.mainLayout = QtWidgets.QGridLayout()
        # self.setLayout(self.mainLayout)
        # self.initUi()
        self.actionType = None
        self.selectedTank = None
        self.start_layout()

        self.receiveBtn.clicked.connect(self.receive)
        self.sendBtn.clicked.connect(self.select_size)
        self.smallBtn.clicked.connect(self.select_small)
        self.mediumBtn.clicked.connect(self.select_medium)
        self.largeBtn.clicked.connect(self.select_large)
        self.confirmBtn.clicked.connect(self.final_confirm)

    def start_layout(self):
        self.receiveBtn.show()
        self.sendBtn.show()
        self.smallBtn.hide()
        self.mediumBtn.hide()
        self.largeBtn.hide()
        self.packageCodeEdit.hide()
        self.packageCodeEdit.clear()
        self.confirmBtn.hide()
        self.phoneNumberEdit.hide()
        self.phoneNumberEdit.clear()
        self.actionType = None
        self.selectedTank = None

    def receive(self):
        self.actionType = self.ActionType.RECEIVE
        self.receiveBtn.hide()
        self.sendBtn.hide()
        self.phoneNumberEdit.show()
        self.packageCodeEdit.show()
        self.confirmBtn.show()

    def select_size(self):
        self.receiveBtn.hide()
        self.sendBtn.hide()
        self.smallBtn.show()
        self.mediumBtn.show()
        self.largeBtn.show()
        self.actionType = self.ActionType.SEND

    def select_large(self):
        self.pm.load_parcel_tanks()
        self.selectedTank = self.pm.propose_free_tank(ParcelTank.ParcelTankSize.LARGE)
        self.select_size_confirm()

    def select_medium(self):
        self.pm.load_parcel_tanks()
        self.selectedTank = self.pm.propose_free_tank(ParcelTank.ParcelTankSize.MEDIUM)
        self.select_size_confirm()

    def select_size_confirm(self):
        if self.selectedTank is None:
            QtWidgets.QMessageBox.warning(self, 'Uwaga', 'Podany rozmiar skrytki jest niedostępny')
            # self.start_layout()
        else:
            self.smallBtn.hide()
            self.mediumBtn.hide()
            self.largeBtn.hide()
            self.phoneNumberEdit.show()
            self.confirmBtn.show()

    def select_small(self):
        self.pm.load_parcel_tanks()
        self.selectedTank = self.pm.propose_free_tank(ParcelTank.ParcelTankSize.SMALL)
        self.select_size_confirm()

    def final_confirm(self):
        self.pm.load_parcel_tanks()
        if self.actionType == self.ActionType.SEND:
            message = self.pm.send_package(self.phoneNumberEdit.text(), self.selectedTank)
        elif self.actionType == self.ActionType.RECEIVE:
            message = self.pm.receive_package(self.phoneNumberEdit.text(), self.packageCodeEdit.text())
        else:
            return
        QtWidgets.QMessageBox.information(self, 'Info', message)
        self.start_layout()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    pmv = ParcelMachineView()
    pmv.setWindowTitle('Parcel Machine View')
    pmv.show()
    app.exec()
