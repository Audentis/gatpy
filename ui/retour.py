# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources\retour-dialog.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(800, 600)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.listWidget = QtGui.QListWidget(Dialog)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.horizontalLayout.addWidget(self.listWidget)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.deleteButton = QtGui.QPushButton(Dialog)
        self.deleteButton.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.deleteButton.setFont(font)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.gridLayout_2.addWidget(self.deleteButton, 1, 0, 1, 1)
        self.closeButton = QtGui.QPushButton(Dialog)
        self.closeButton.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.closeButton.setFont(font)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.gridLayout_2.addWidget(self.closeButton, 1, 1, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.listWidget_2 = QtGui.QListWidget(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.listWidget_2.setFont(font)
        self.listWidget_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.listWidget_2.setObjectName(_fromUtf8("listWidget_2"))
        self.horizontalLayout_3.addWidget(self.listWidget_2)
        self.listWidget_4 = QtGui.QListWidget(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.listWidget_4.setFont(font)
        self.listWidget_4.setFrameShape(QtGui.QFrame.NoFrame)
        self.listWidget_4.setObjectName(_fromUtf8("listWidget_4"))
        self.horizontalLayout_3.addWidget(self.listWidget_4)
        self.listWidget_3 = QtGui.QListWidget(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.listWidget_3.setFont(font)
        self.listWidget_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.listWidget_3.setObjectName(_fromUtf8("listWidget_3"))
        self.horizontalLayout_3.addWidget(self.listWidget_3)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)
        self.horizontalLayout_3.setStretch(2, 2)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 2)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Retour", None))
        self.deleteButton.setText(_translate("Dialog", "Verwijderen", None))
        self.closeButton.setText(_translate("Dialog", "Annuleren", None))

