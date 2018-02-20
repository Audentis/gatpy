import csv
import os

from PyQt4 import QtGui

from gatpy.logging import logger
from ui.retour import Ui_Dialog


class RetourDialog(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.cart = parent.cart

        self.setupUi(self)
        self.setFixedSize(800, 600)
        self.connectAll()
        self.loadData()

    def connectAll(self):
        self.closeButton.clicked.connect(self.close)

    def loadData(self):
        with open(self.cart.filename, 'r') as f:
            for row in reversed(list(csv.reader(f))):
                print(row)
