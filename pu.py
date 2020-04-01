import sys
import PU_ui, add_PU_ui, click_PU_ui, replace_PU_ui
    
from PyQt5 import QtCore, QtGui, QtWidgets
        
class Pu(QtWidgets.QWidget, PU_ui.Ui_Form):
    def __init__(self, conn, id_kpu):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('ПУ')
        self.conn = conn
        self.pushButton_add.clicked.connect(self.add_window)
        self.tableWidget_scaut.doubleClicked.connect(self.cell_was_clicked)        
        self.scaut_query()
        self.filtr_city()
        self.pushButton_filtr.clicked.connect(self.scaut_query)
        self.tableWidget_scaut.horizontalHeader().hideSection(4)
        self.show() 

    def add_window(self):
        self.add_pu = add_Pu()

    def clik_pu(self):
        self.click_pu = click_Pu()

class add_Pu(QtWidgets.QWidget, add_PU_ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Добавить ПУ')
        self.show()
        self.pushButton_addStart.clicked.connect(self.add_start)
        self.pushButton_save.clicked.connect(self.save)

    def save(self):
        self.close()

    def add_start(self):
        self.close()

class click_Pu(QtWidgets.QWidget, click_PU_ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('ПУ')
        self.show()
        self.pushButton_replace.clicked.connect(self.replace)
        self.pushButton_save.clicked.connect(self.save)
        self.pushButton_addStart.clicked.connect(self.add_start)

    def save(self):
        self.close()

    def replace(self):
        self.replace_pu = replace_Pu()
        self.close()
        
    def add_start(self):
        self.close()
        
class replace_Pu(QtWidgets.QWidget, replace_PU_ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Замена ПУ')
        self.show()
        self.pushButton_replace.clicked.connect(self.replace)
        self.pushButton_cansel.clicked.connect(self.cansel)

    def cansel(self):
        self.close()

    def replace(self):
        self.close()


