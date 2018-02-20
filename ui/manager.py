# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources\manager.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(300, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(_fromUtf8("*{\n"
"    color: #f8f8f2;\n"
"    background: #272822;\n"
"}\n"
"QPushButton{\n"
"    background: #141411;\n"
"}\n"
"QLineEdit{\n"
"    background: #383830;\n"
"    border: 1px solid #595959;\n"
"}\n"
"QListView,\n"
"QTreeView{\n"
"    background: #383830;\n"
"}\n"
"QListView::item:selected,\n"
"QTreeView::item:selected{\n"
"    background: #141411;\n"
"}\n"
"QTreeView::item:selected:!active {\n"
"    color: white;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #616161, stop: 0.5 #505050,\n"
"                                      stop: 0.6 #434343, stop:1 #656565);\n"
"}\n"
"QMenuBar{\n"
"    background: #383830;\n"
"}\n"
"QMenuBar::item{\n"
"    background-color: transparent;\n"
"}"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.widget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(128, 128))
        self.widget.setStyleSheet(_fromUtf8("border-image: url(:icon.ico);"))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.exportButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportButton.sizePolicy().hasHeightForWidth())
        self.exportButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.exportButton.setFont(font)
        self.exportButton.setObjectName(_fromUtf8("exportButton"))
        self.verticalLayout.addWidget(self.exportButton)
        self.multiExportButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.multiExportButton.sizePolicy().hasHeightForWidth())
        self.multiExportButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.multiExportButton.setFont(font)
        self.multiExportButton.setObjectName(_fromUtf8("multiExportButton"))
        self.verticalLayout.addWidget(self.multiExportButton)
        self.manageProductsButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manageProductsButton.sizePolicy().hasHeightForWidth())
        self.manageProductsButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.manageProductsButton.setFont(font)
        self.manageProductsButton.setObjectName(_fromUtf8("manageProductsButton"))
        self.verticalLayout.addWidget(self.manageProductsButton)
        self.quitButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quitButton.sizePolicy().hasHeightForWidth())
        self.quitButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.quitButton.setFont(font)
        self.quitButton.setObjectName(_fromUtf8("quitButton"))
        self.verticalLayout.addWidget(self.quitButton)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "GatManager", None))
        self.exportButton.setText(_translate("MainWindow", "Verwerk laatste rapport", None))
        self.multiExportButton.setText(_translate("MainWindow", "Verwerk meerdere rapporten", None))
        self.manageProductsButton.setText(_translate("MainWindow", "Productbeheer", None))
        self.quitButton.setText(_translate("MainWindow", "Afsluiten", None))

from . import resource_rc
