# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scaut.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(1080, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_city = QtWidgets.QLabel(Form)
        self.label_city.setObjectName("label_city")
        self.horizontalLayout.addWidget(self.label_city)
        self.comboBox_city = QtWidgets.QComboBox(Form)
        self.comboBox_city.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox_city.setEditable(False)
        self.comboBox_city.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox_city.setDuplicatesEnabled(False)
        self.comboBox_city.setObjectName("comboBox_city")
        self.horizontalLayout.addWidget(self.comboBox_city)
        self.label_street = QtWidgets.QLabel(Form)
        self.label_street.setObjectName("label_street")
        self.horizontalLayout.addWidget(self.label_street)
        self.comboBox_street = QtWidgets.QComboBox(Form)
        self.comboBox_street.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox_street.setObjectName("comboBox_street")
        self.horizontalLayout.addWidget(self.comboBox_street)
        self.label_house = QtWidgets.QLabel(Form)
        self.label_house.setObjectName("label_house")
        self.horizontalLayout.addWidget(self.label_house)
        self.comboBox_house = QtWidgets.QComboBox(Form)
        self.comboBox_house.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox_house.setObjectName("comboBox_house")
        self.horizontalLayout.addWidget(self.comboBox_house)
        self.label_entrance = QtWidgets.QLabel(Form)
        self.label_entrance.setObjectName("label_entrance")
        self.horizontalLayout.addWidget(self.label_entrance)
        self.comboBox_entrance = QtWidgets.QComboBox(Form)
        self.comboBox_entrance.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox_entrance.setObjectName("comboBox_entrance")
        self.horizontalLayout.addWidget(self.comboBox_entrance)
        self.pushButton_filtr = QtWidgets.QPushButton(Form)
        self.pushButton_filtr.setObjectName("pushButton_filtr")
        self.horizontalLayout.addWidget(self.pushButton_filtr)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_add = QtWidgets.QPushButton(Form)
        self.pushButton_add.setObjectName("pushButton_add")
        self.horizontalLayout.addWidget(self.pushButton_add)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget_scaut = QtWidgets.QTableWidget(Form)
        self.tableWidget_scaut.setEnabled(True)
        self.tableWidget_scaut.setSizeIncrement(QtCore.QSize(0, 0))
        self.tableWidget_scaut.setMouseTracking(True)
        self.tableWidget_scaut.setTabletTracking(False)
        self.tableWidget_scaut.setAcceptDrops(False)
        self.tableWidget_scaut.setLineWidth(1)
        self.tableWidget_scaut.setMidLineWidth(0)
        self.tableWidget_scaut.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_scaut.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_scaut.setShowGrid(True)
        self.tableWidget_scaut.setObjectName("tableWidget_scaut")
        self.tableWidget_scaut.setColumnCount(5)
        self.tableWidget_scaut.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_scaut.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_scaut.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_scaut.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_scaut.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_scaut.setHorizontalHeaderItem(4, item)
        self.tableWidget_scaut.horizontalHeader().setVisible(True)
        self.tableWidget_scaut.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_scaut.horizontalHeader().setDefaultSectionSize(170)
        self.tableWidget_scaut.horizontalHeader().setHighlightSections(True)
        self.tableWidget_scaut.horizontalHeader().setMinimumSectionSize(50)
        self.tableWidget_scaut.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget_scaut.horizontalHeader().setStretchLastSection(False)
        self.tableWidget_scaut.verticalHeader().setVisible(True)
        self.tableWidget_scaut.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget_scaut.verticalHeader().setDefaultSectionSize(37)
        self.tableWidget_scaut.verticalHeader().setHighlightSections(True)
        self.tableWidget_scaut.verticalHeader().setMinimumSectionSize(30)
        self.tableWidget_scaut.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget_scaut.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tableWidget_scaut)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_city.setText(_translate("Form", "Город"))
        self.label_street.setText(_translate("Form", "Улица"))
        self.label_house.setText(_translate("Form", "Дом"))
        self.label_entrance.setText(_translate("Form", "Подъезд"))
        self.pushButton_filtr.setText(_translate("Form", "Обновить"))
        self.pushButton_add.setText(_translate("Form", "Добавить"))
        self.tableWidget_scaut.setSortingEnabled(True)
        item = self.tableWidget_scaut.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Город"))
        item = self.tableWidget_scaut.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Улица"))
        item = self.tableWidget_scaut.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Дом"))
        item = self.tableWidget_scaut.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Подъезд"))
        item = self.tableWidget_scaut.horizontalHeaderItem(4)
        item.setText(_translate("Form", "id_entr"))
