# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connected_BD.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(200, 177)
        self.formLayout_2 = QtWidgets.QFormLayout(Form)
        self.formLayout_2.setObjectName("formLayout_2")
        self.pushButton_continue = QtWidgets.QPushButton(Form)
        self.pushButton_continue.setObjectName("pushButton_continue")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.pushButton_continue)
        self.lineEdit_port = QtWidgets.QLineEdit(Form)
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_port)
        self.label_port = QtWidgets.QLabel(Form)
        self.label_port.setObjectName("label_port")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_port)
        self.lineEdit_host = QtWidgets.QLineEdit(Form)
        self.lineEdit_host.setObjectName("lineEdit_host")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_host)
        self.lineEdit_password = QtWidgets.QLineEdit(Form)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_password)
        self.lineEdit_user = QtWidgets.QLineEdit(Form)
        self.lineEdit_user.setObjectName("lineEdit_user")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_user)
        self.label_host = QtWidgets.QLabel(Form)
        self.label_host.setObjectName("label_host")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_host)
        self.label_password = QtWidgets.QLabel(Form)
        self.label_password.setObjectName("label_password")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_password)
        self.label_user = QtWidgets.QLabel(Form)
        self.label_user.setObjectName("label_user")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_user)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(5, QtWidgets.QFormLayout.FieldRole, spacerItem)
        self.lineEdit_database = QtWidgets.QLineEdit(Form)
        self.lineEdit_database.setObjectName("lineEdit_database")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_database)
        self.label_database = QtWidgets.QLabel(Form)
        self.label_database.setObjectName("label_database")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_database)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_continue.setText(_translate("Form", "Продолжить"))
        self.lineEdit_port.setText(_translate("Form", "5432"))
        self.label_port.setText(_translate("Form", "port"))
        self.lineEdit_host.setText(_translate("Form", "192.168.105.30"))
        self.lineEdit_password.setText(_translate("Form", "counters"))
        self.lineEdit_user.setText(_translate("Form", "counters"))
        self.label_host.setText(_translate("Form", "host"))
        self.label_password.setText(_translate("Form", "password"))
        self.label_user.setText(_translate("Form", "user"))
        self.lineEdit_database.setText(_translate("Form", "counters"))
        self.label_database.setText(_translate("Form", "database"))
