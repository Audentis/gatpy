from collections import OrderedDict
import locale
import os
import sys
from math import ceil

from PyQt4 import QtGui
from PyQt4 import QtCore

from gatpy import logging
from gatpy.cart import Cart, Method
from gatpy.config import get_data_dir
from gatpy.gui.retour import RetourDialog
from gatpy.gui.whack import WhackDialog
from gatpy.logging import logger
from gatpy.products import Products
from ui.main import Ui_MainWindow

FUNCTIONS_NAME = 'Functies'
FUNCTIONS_PAGE =  ['Opmerking',
                   'Retour',
                   'EV',
                   'Retour EV',
                   'Naborrel',
                   'Retour naborrel',
                   'Regel verwijderen',
                   'Retour laatste']

UNPROCESSED_STYLE = 'background: #58C141; color: #1D4015'
PROCESSED_STYLE = 'background: #C14B45; color: #401917'


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.products = Products(os.path.join(get_data_dir(), "products.csv"))
        self.cart = Cart(self.products)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.buildButtonGroups()
        self.buildPages()

        self.connectAll()

        logging.setStatusbar(self.ui.statusBar)

        self.setPage(list(self.pages.keys())[1])
        self.setCategoryPage(0)

    def buildButtonGroups(self):
        self.ui.numpadButtons = []
        for i in range(self.ui.npGrid.count()):
            obj = self.ui.npGrid.itemAt(i).widget()
            if obj.text().isdigit():
                self.ui.numpadButtons.append(obj)

        self.ui.productButtons = []
        for i in range(self.ui.leftProductButtons.count()):
            self.ui.productButtons.append(self.ui.leftProductButtons.itemAt(i).widget())
            self.ui.productButtons.append(self.ui.rightProductButtons.itemAt(i).widget())

        self.ui.categoryButtons = []
        for i in range(self.ui.categoryLayout.count()):
            obj = self.ui.categoryLayout.itemAt(i).widget()
            if isinstance(obj, QtGui.QPushButton):
                self.ui.categoryButtons.append(obj)

    def buildPages(self):
        self.pages = OrderedDict()
        self.category_pages = OrderedDict()

        self.pages[FUNCTIONS_NAME] = FUNCTIONS_PAGE

        categories = self.products.categories()
        for category in categories:
            products = self.products.category_dict()[category]
            num_pages = ceil(len(products) / len(self.ui.productButtons))
            for i in range(num_pages):
                p2add = range(len(self.ui.productButtons)*i, len(self.ui.productButtons)*(i+1))

                if num_pages == 1:
                    name = category.capitalize()
                else:
                    name = category.capitalize() + ' ' + str(i + 1)
                self.pages[name] = []
                for j in p2add:
                    try:
                        self.pages[name].append(products[j])
                    except IndexError:
                        pass

        num_category_pages = ceil(len(self.pages) / len (self.ui.categoryButtons))
        for i in range(num_category_pages):
            p2add = range(len(self.ui.categoryButtons)*i, len(self.ui.categoryButtons)*(i+1))
            self.category_pages[i] = []
            for j in p2add:
                try:
                    page_name = list(self.pages.keys())[j]
                    self.category_pages[i].append(page_name)
                except IndexError:
                    pass

    def connectAll(self):
        # menuBar
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionFullscreen.triggered.connect(self.showFullScreen)
        self.ui.actionWindowed.triggered.connect(self.showMaximized)
        self.ui.actionGame.triggered.connect(self.openWhack)

        self.ui.amountList.clicked.connect(self.selectSameLine)
        self.ui.productList.clicked.connect(self.selectSameLine)
        self.ui.priceList.clicked.connect(self.selectSameLine)

        # numpad
        for button in self.ui.numpadButtons:
            button.clicked.connect(self.numpadInput)
        self.ui.numpadClearButton.clicked.connect(self.numpadClear)
        self.ui.numpadBackspaceButton.clicked.connect(self.numpadBackspace)

        self.ui.payCashButton.clicked.connect(self.payCash)
        self.ui.payPinButton.clicked.connect(self.payPin)

        # categories
        for button in self.ui.categoryButtons:
            button.clicked.connect(self.switchCategory)
        self.ui.prevBtn.clicked.connect(self.prevCategory)
        self.ui.nextBtn.clicked.connect(self.nextCategory)

        # products
        for button in self.ui.productButtons:
            button.clicked.connect(self.addProduct)

    def openWhack(self):
        whack = WhackDialog(self)
        whack.show()

    def openRetour(self):
        retour = RetourDialog(self)
        retour.show()

    def selectSameLine(self, index):
        row = index.row()
        self.ui.amountList.setCurrentItem(self.ui.amountList.item(row))
        self.ui.productList.setCurrentItem(self.ui.productList.item(row))
        self.ui.priceList.setCurrentItem(self.ui.priceList.item(row))

    def numpadInput(self):
        input = self.sender().text()

        if self.ui.numpadLineEdit.text() == "" and input == "0":
            return

        self.ui.numpadLineEdit.insert(input)

    def numpadClear(self):
        self.ui.numpadLineEdit.clear()

    def numpadBackspace(self):
        self.ui.numpadLineEdit.backspace()

    def payCash(self):
        self.pay(Method.CASH)

    def payPin(self):
        self.pay(Method.PIN)

    def switchCategory(self):
        self.setPage(self.sender().text())

    def prevCategory(self):
        self.setCategoryPage(self.current_category_page - 1)

    def nextCategory(self):
        self.setCategoryPage(self.current_category_page + 1)

    def addProduct(self):
        name = self.sender().text()

        if self.current_page == FUNCTIONS_NAME:
            return self.callFunction(name)

        if self.cart.isCheckedOut():
            self.cart.clear()

        product = self.products.dict()[name]
        self.cart.add(self.getNumpad(), product)
        self.numpadClear()
        self.updateReceipt()

    def setPage(self, page_name):
        page = self.pages[page_name]
        self.current_page = page_name

        for i, button in enumerate(self.ui.productButtons):
            try:
                name = page[i].name if hasattr(page[i], 'name') else page[i]
                button.setText(name)
                button.setEnabled(True)
                button.setFlat(False)
            except IndexError:
                button.setText("")
                button.setEnabled(False)
                button.setFlat(True)

    def setCategoryPage(self, page_num):
        page = self.category_pages[page_num]
        self.current_category_page = page_num

        for i, button in enumerate(self.ui.categoryButtons):
            try:
                button.setText(page[i])
                button.setEnabled(True)
                button.setFlat(False)
            except IndexError:
                button.setText("")
                button.setEnabled(False)
                button.setFlat(True)

        if page_num < len(self.category_pages) - 1:
            self.ui.nextBtn.setEnabled(True)
        else:
            self.ui.nextBtn.setEnabled(False)

        if page_num > 0:
            self.ui.prevBtn.setEnabled(True)
        else:
            self.ui.prevBtn.setEnabled(False)

    def callFunction(self, function):
        if function == "Opmerking":
            self.comment()
        elif function == "Retour":
            self.pay(Method.CASH, retour=True)
        elif function == "EV":
            self.pay(Method.EV)
        elif function == "Retour EV":
            self.pay(Method.EV, retour=True)
        elif function == "Naborrel":
            self.pay(Method.NABORREL)
        elif function == "Retour naborrel":
            self.pay(Method.NABORREL, retour=True)
        elif function == "Regel verwijderen":
            self.removeLine()
        elif function == "Retour laatste":
            self.openRetour()

    def getNumpad(self):
        numpad = self.ui.numpadLineEdit.text()
        return 1 if numpad == "" else int(numpad)

    def removeLine(self):
        if self.cart.isCheckedOut():
            logger.warn("Deze transactie is al afgerekend")
            return

        item = self.ui.amountList.selectedItems()

        if not item:
            logger.warn("Geen regel geselecteerd")
            return

        row = self.ui.amountList.row(item[0])
        self.cart.contents.pop(row)
        self.updateReceipt()

    def comment(self):
        comment, ok = QtGui.QInputDialog.getText(self, "Opmerking", "Voer opmerking in")
        if ok and comment:
            self.cart.addCommentToFile(comment)

    def updateReceipt(self):
        self.ui.amountList.setStyleSheet(UNPROCESSED_STYLE)
        self.ui.productList.setStyleSheet(UNPROCESSED_STYLE)
        self.ui.priceList.setStyleSheet(UNPROCESSED_STYLE)
        self.ui.totalAmountLineEdit.setStyleSheet(UNPROCESSED_STYLE)
        self.ui.totalPriceLineEdit.setStyleSheet(UNPROCESSED_STYLE)

        self.ui.amountList.clear()
        self.ui.productList.clear()
        self.ui.priceList.clear()

        for entry in self.cart.contents:
            self.ui.amountList.addItem(str(entry[0]))
            self.ui.productList.addItem(entry[1])
            item = QtGui.QListWidgetItem(locale.currency(entry[2]))
            item.setTextAlignment(QtCore.Qt.AlignRight)
            self.ui.priceList.addItem(item)

        total = self.cart.total()
        self.ui.totalAmountLineEdit.setText(str(total[0]))
        self.ui.totalPriceLineEdit.setText(locale.currency(total[1]))

    def pay(self, method, retour=False):
        if self.cart.isCheckedOut():
            return logger.warn('Deze transactie is al afgerekend')

        if self.cart.isEmpty():
            return

        self.lastMethod = method

        if retour:
            self.cart.negate()
            self.updateReceipt()

        self.cart.checkOut(method)

        self.ui.amountList.setStyleSheet(PROCESSED_STYLE)
        self.ui.productList.setStyleSheet(PROCESSED_STYLE)
        self.ui.priceList.setStyleSheet(PROCESSED_STYLE)
        self.ui.totalAmountLineEdit.setStyleSheet(PROCESSED_STYLE)
        self.ui.totalPriceLineEdit.setStyleSheet(PROCESSED_STYLE)

        self.setPage(list(self.pages.keys())[1])


def main():
    locale.setlocale(locale.LC_ALL, '')

    log_dir = os.path.join(get_data_dir(), "log")
    logging.init(log_dir)

    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.resize(1024, 768)
    myapp.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
