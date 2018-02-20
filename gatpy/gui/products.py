import os

from PyQt4 import QtGui

from gatpy.config import get_data_dir
from gatpy.products import Product, Products
from ui.products import Ui_Dialog


class ProductsDialog(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.selection = -1

        self.setupUi(self)
        self.setFixedSize(800, 600)
        self.connectAll()
        self.buildModel()

    def connectAll(self):
        self.treeView.clicked.connect(self.showProduct)
        self.saveButton.clicked.connect(self.saveProduct)
        self.deleteButton.clicked.connect(self.destroyProduct)
        self.newButton.clicked.connect(self.newProduct)
        self.exportButton.clicked.connect(self.saveProducts)
        self.quitButton.clicked.connect(self.close)

    def showProduct(self, index):
        self.selection = index.row()
        self.nameLineEdit.setText(self.products.item(self.selection, 0).text())
        self.priceLineEdit.setText(self.products.item(self.selection, 1).text())
        self.groupLineEdit.setText(self.products.item(self.selection, 2).text())
        self.categoryLineEdit.setText(self.products.item(self.selection, 3).text())

    def saveProduct(self):
        self.products.setItem(self.selection, 0, QtGui.QStandardItem(self.nameLineEdit.text()))
        self.products.setItem(self.selection, 1, QtGui.QStandardItem(self.priceLineEdit.text()))
        self.products.setItem(self.selection, 2, QtGui.QStandardItem(self.groupLineEdit.text()))
        self.products.setItem(self.selection, 3, QtGui.QStandardItem(self.categoryLineEdit.text()))
        self.clearForm()

    def destroyProduct(self):
        self.products.removeRow(self.selection)
        self.clearForm()

    def newProduct(self):
        self.products.appendRow([
            QtGui.QStandardItem(self.nameLineEdit.text()),
            QtGui.QStandardItem(self.priceLineEdit.text()),
            QtGui.QStandardItem(self.groupLineEdit.text()),
            QtGui.QStandardItem(self.categoryLineEdit.text()),
        ])
        self.clearForm()

    def saveProducts(self):
        products = []

        for i in range(self.products.rowCount()):
            products.append(
                Product(
                    self.products.item(i, 0).text(),
                    self.products.item(i, 1).text(),
                    self.products.item(i, 2).text(),
                    self.products.item(i, 3).text(),
                )
            )

        self.productDb.products = products
        self.productDb.save()

        QtGui.QMessageBox.information(self, "Exporteren succesvol", "De producten zijn succesvol geëxporteerd.")

    def clearForm(self):
        self.nameLineEdit.clear()
        self.priceLineEdit.clear()
        self.groupLineEdit.clear()
        self.categoryLineEdit.clear()

    def buildModel(self):
        self.productDb = Products(os.path.join(get_data_dir(), "products.csv"))

        self.products = QtGui.QStandardItemModel()
        self.products.setHorizontalHeaderLabels([
            "Naam", "Prijs", "Kostenplaats", "Categorie"
        ])

        for product in self.productDb.products:
            self.products.appendRow([
                QtGui.QStandardItem(product.name),
                QtGui.QStandardItem(product.price),
                QtGui.QStandardItem(product.group),
                QtGui.QStandardItem(product.category),
            ])

        self.treeView.setModel(self.products)
        self.treeView.resizeColumnToContents(0)
        self.treeView.resizeColumnToContents(1)
