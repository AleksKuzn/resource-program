# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(449, 350)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 449, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_analysis = QtWidgets.QMenu(self.menubar)
        self.menu_analysis.setObjectName("menu_analysis")
        MainWindow.setMenuBar(self.menubar)
        self.action_scaut = QtWidgets.QAction(MainWindow)
        self.action_scaut.setObjectName("action_scaut")
        self.action_kpu = QtWidgets.QAction(MainWindow)
        self.action_kpu.setObjectName("action_kpu")
        self.action_pu = QtWidgets.QAction(MainWindow)
        self.action_pu.setObjectName("action_pu")
        self.action_quit = QtWidgets.QAction(MainWindow)
        self.action_quit.setObjectName("action_quit")
        self.menu.addAction(self.action_scaut)
        self.menu.addAction(self.action_kpu)
        self.menu.addAction(self.action_pu)
        self.menu.addAction(self.action_quit)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_analysis.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "Оборудование"))
        self.menu_analysis.setTitle(_translate("MainWindow", "Анализ данных"))
        self.action_scaut.setText(_translate("MainWindow", "СКАУТ"))
        self.action_kpu.setText(_translate("MainWindow", "КПУ"))
        self.action_pu.setText(_translate("MainWindow", "ПУ"))
        self.action_quit.setText(_translate("MainWindow", "Выход"))
