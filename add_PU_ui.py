# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_PU.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(505, 339)
        Form.setMinimumSize(QtCore.QSize(479, 269))
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 491, 321))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 461, 271))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setObjectName("formLayout_6")
        self.label_17 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_17.setObjectName("label_17")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_17)
        self.lineEdit_17 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_17)
        self.label_18 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_18.setObjectName("label_18")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.lineEdit_18 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_18)
        self.label_19 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_19.setObjectName("label_19")
        self.formLayout_6.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_19)
        self.label_20 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_20.setObjectName("label_20")
        self.formLayout_6.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_20)
        self.lineEdit_20 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.formLayout_6.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_20)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout_6.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout_6.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout_6.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout_6.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(12)
        self.spinBox.setObjectName("spinBox")
        self.formLayout_6.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.horizontalLayout_3.addLayout(self.formLayout_6)
        self.formLayout_9 = QtWidgets.QFormLayout()
        self.formLayout_9.setObjectName("formLayout_9")
        self.label_29 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_29.setObjectName("label_29")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_29)
        self.lineEdit_29 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_29.setObjectName("lineEdit_29")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_29)
        self.label_30 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_30.setObjectName("label_30")
        self.formLayout_9.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_30)
        self.lineEdit_30 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_30.setObjectName("lineEdit_30")
        self.formLayout_9.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_30)
        self.label_32 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_32.setObjectName("label_32")
        self.formLayout_9.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_32)
        self.lineEdit_32 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_32.setObjectName("lineEdit_32")
        self.formLayout_9.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_32)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout_9.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout_9.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout_9.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.formLayout_9.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_4)
        self.horizontalLayout_3.addLayout(self.formLayout_9)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_2.addWidget(self.checkBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButton_save = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout.addWidget(self.pushButton_save)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 481, 291))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableView = QtWidgets.QTableView(self.verticalLayoutWidget_2)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_2.addWidget(self.tableView)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_7.addWidget(self.label_7)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout_6.addWidget(self.lineEdit_5)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.horizontalLayout_6.addWidget(self.lineEdit_6)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.horizontalLayout_6.addWidget(self.lineEdit_7)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.pushButton_addStart = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_addStart.setObjectName("pushButton_addStart")
        self.horizontalLayout_5.addWidget(self.pushButton_addStart)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_17.setText(_translate("Form", "№ Кв."))
        self.label_18.setText(_translate("Form", "S/N КПУ"))
        self.label_19.setText(_translate("Form", "Клемма"))
        self.label_20.setText(_translate("Form", "Сер.Ном"))
        self.label_2.setText(_translate("Form", "Тип"))
        self.label_3.setText(_translate("Form", "Модель"))
        self.label_29.setText(_translate("Form", "коэффициент"))
        self.label_30.setText(_translate("Form", "показания"))
        self.label_32.setText(_translate("Form", "дата подключения"))
        self.label.setText(_translate("Form", "дата отключения"))
        self.label_4.setText(_translate("Form", "Примечания"))
        self.checkBox.setText(_translate("Form", "работоспособность"))
        self.pushButton_save.setText(_translate("Form", "Сохранить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Информация"))
        self.label_6.setText(_translate("Form", "Дата"))
        self.label_5.setText(_translate("Form", "Показания"))
        self.label_7.setText(_translate("Form", "Импульсы"))
        self.pushButton_addStart.setText(_translate("Form", "Добавить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Стартовое значение"))
