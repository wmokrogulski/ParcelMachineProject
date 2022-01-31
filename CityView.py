import sqlite3
import sys
from functools import partial

from PyQt6 import QtWidgets, QtGui, QtCore


class CityView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CityView, self).__init__(parent)
        self.setLayout(QtWidgets.QGridLayout())
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        style = """     CityView {
                        border-image: url(images/mapa_dzielnic_bez_nazw.png);
                        }
                        CityView QPushButton {
                        color: green;
                        background-color:none;
                        border:none;
                        }
                        """
        self.setStyleSheet(style)
        self.districts = []
        self.districtBtns = []
        self.load_districts()
        self.add_district_btns()

    def load_districts(self):
        self.districts.clear()
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        for district in c.execute("select rowid, name from districts"):
            self.districts.append(district[1])

    def add_district_btns(self):
        # mover=[0,0]
        i = 0
        j = 0
        cols = 4
        for district in self.districts:
            districtBtn = QtWidgets.QPushButton(district)
            districtBtn.clicked.connect(partial(self.btn_test, district))
            self.layout().addWidget(districtBtn, i, j)
            self.districtBtns.append(districtBtn)
            i += 1
            if i == cols:
                j += 1
                i = 0

    def btn_test(self, btn_name):
        print(btn_name)
        if self.parent() is not None:
            self.parent().setDistrictView((btn_name))

            # self.layout().addWidget(districtBtn)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    cv = CityView()
    cv.setWindowTitle('City View')
    cv.show()
    app.exec()
