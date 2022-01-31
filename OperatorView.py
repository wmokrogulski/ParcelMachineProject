import sqlite3
import sys
from enum import Enum
from functools import partial

from PyQt6 import QtWidgets, QtGui, QtCore

from events import get_event_by_id
from operator_view.Ui_OperatorView import Ui_Form


class OperatorView(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(OperatorView, self).__init__(parent)
        self.setupUi(self)
        self.parcelMachineTable_2.setRowCount(1)
        self.parcelMachineTable_2.setItem(0, 0, QtWidgets.QTableWidgetItem('Test'))
        self.orderRepairBtn.clicked.connect(self.order_repair)

    def order_repair(self):
        row=int(self.parcelMachineTable_2.currentRow())
        if row==-1:
            return
        print(self.parcelMachineTable_2.item(row,0).text())

    def loadLogs(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('select rowid from events')
        rows=c.fetchall()
        conn.close()
        row_count=0
        for row in rows:
            event=get_event_by_id(row[0])
            row_count+=1
            self.logsTable.setRowCount(row_count)
            self.logsTable.setItem()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ov = OperatorView()
    ov.setWindowTitle('Operator View')
    ov.show()
    app.exec()
