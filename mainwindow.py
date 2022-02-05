# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(844, 534)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.select_hex_file = QtWidgets.QPushButton(self.centralwidget)
        self.select_hex_file.setGeometry(QtCore.QRect(30, 40, 231, 51))
        self.select_hex_file.setObjectName("select_hex_file")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 190, 791, 311))
        self.textEdit.setObjectName("textEdit")
        self.create_bin2hash = QtWidgets.QPushButton(self.centralwidget)
        self.create_bin2hash.setGeometry(QtCore.QRect(290, 40, 251, 51))
        self.create_bin2hash.setObjectName("create_bin2hash")
        self.clear = QtWidgets.QPushButton(self.centralwidget)
        self.clear.setGeometry(QtCore.QRect(30, 120, 231, 51))
        self.clear.setObjectName("clear")
        self.create_signature_without_key = QtWidgets.QPushButton(self.centralwidget)
        self.create_signature_without_key.setGeometry(QtCore.QRect(290, 120, 251, 51))
        self.create_signature_without_key.setObjectName("create_signature_without_key")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(560, 30, 51, 41))
        self.label.setObjectName("label")
        self.public_key = QtWidgets.QLineEdit(self.centralwidget)
        self.public_key.setGeometry(QtCore.QRect(660, 40, 161, 21))
        self.public_key.setObjectName("public_key")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(560, 70, 61, 41))
        self.label_2.setObjectName("label_2")
        self.private_key = QtWidgets.QLineEdit(self.centralwidget)
        self.private_key.setGeometry(QtCore.QRect(660, 80, 161, 21))
        self.private_key.setObjectName("private_key")
        self.create_signature_using_key = QtWidgets.QPushButton(self.centralwidget)
        self.create_signature_using_key.setGeometry(QtCore.QRect(560, 130, 261, 31))
        self.create_signature_using_key.setObjectName("create_signature_using_key")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 844, 22))
        self.menubar.setObjectName("menubar")
        self.menuMainWindow = QtWidgets.QMenu(self.menubar)
        self.menuMainWindow.setObjectName("menuMainWindow")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuMainWindow.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.select_hex_file.setText(_translate("MainWindow", "请选择文件(hex)文件"))
        self.create_bin2hash.setText(_translate("MainWindow", "从bin文件生成hash(boot or app)"))
        self.clear.setText(_translate("MainWindow", "生成数组"))
        self.create_signature_without_key.setText(_translate("MainWindow", "生成签名(生成新公私钥对)"))
        self.label.setText(_translate("MainWindow", "公钥：0x"))
        self.label_2.setText(_translate("MainWindow", "私钥：0x"))
        self.create_signature_using_key.setText(_translate("MainWindow", "根据已有公私钥对生成签名"))
        self.menuMainWindow.setTitle(_translate("MainWindow", "Signature"))
