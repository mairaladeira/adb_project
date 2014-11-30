# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sun Nov 30 20:18:47 2014
#      by: PyQt4 UI code generator 4.11.3
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
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.buttonClear = QtGui.QPushButton(self.centralwidget)
        self.buttonClear.setGeometry(QtCore.QRect(220, 470, 75, 23))
        self.buttonClear.setObjectName(_fromUtf8("buttonClear"))
        self.buttonAdd = QtGui.QPushButton(self.centralwidget)
        self.buttonAdd.setGeometry(QtCore.QRect(580, 100, 75, 23))
        self.buttonAdd.setObjectName(_fromUtf8("buttonAdd"))
        self.buttonRemove = QtGui.QPushButton(self.centralwidget)
        self.buttonRemove.setGeometry(QtCore.QRect(660, 100, 75, 23))
        self.buttonRemove.setObjectName(_fromUtf8("buttonRemove"))
        self.listView = QtGui.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(530, 130, 256, 331))
        self.listView.setObjectName(_fromUtf8("listView"))
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(50, 189, 120, 181))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 118, 179))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 40, 568, 25))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.buttonNewDBSession = QtGui.QPushButton(self.layoutWidget)
        self.buttonNewDBSession.setObjectName(_fromUtf8("buttonNewDBSession"))
        self.horizontalLayout.addWidget(self.buttonNewDBSession)
        self.buttonNewNoDBSession = QtGui.QPushButton(self.layoutWidget)
        self.buttonNewNoDBSession.setObjectName(_fromUtf8("buttonNewNoDBSession"))
        self.horizontalLayout.addWidget(self.buttonNewNoDBSession)
        self.buttonOpen = QtGui.QPushButton(self.layoutWidget)
        self.buttonOpen.setObjectName(_fromUtf8("buttonOpen"))
        self.horizontalLayout.addWidget(self.buttonOpen)
        self.buttonOpenTANEOutput = QtGui.QPushButton(self.layoutWidget)
        self.buttonOpenTANEOutput.setObjectName(_fromUtf8("buttonOpenTANEOutput"))
        self.horizontalLayout.addWidget(self.buttonOpenTANEOutput)
        self.buttonSave = QtGui.QPushButton(self.layoutWidget)
        self.buttonSave.setObjectName(_fromUtf8("buttonSave"))
        self.horizontalLayout.addWidget(self.buttonSave)
        self.buttonShowDBConfiguration = QtGui.QPushButton(self.layoutWidget)
        self.buttonShowDBConfiguration.setObjectName(_fromUtf8("buttonShowDBConfiguration"))
        self.horizontalLayout.addWidget(self.buttonShowDBConfiguration)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.buttonClear.setText(_translate("MainWindow", "Clear", None))
        self.buttonAdd.setText(_translate("MainWindow", "Add", None))
        self.buttonRemove.setText(_translate("MainWindow", "Remove", None))
        self.buttonNewDBSession.setText(_translate("MainWindow", "NewDBSession", None))
        self.buttonNewNoDBSession.setText(_translate("MainWindow", "NewNoDBSession", None))
        self.buttonOpen.setText(_translate("MainWindow", "Open", None))
        self.buttonOpenTANEOutput.setText(_translate("MainWindow", "Open TANE Output", None))
        self.buttonSave.setText(_translate("MainWindow", "Save", None))
        self.buttonShowDBConfiguration.setText(_translate("MainWindow", "Show DB Configuration", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

