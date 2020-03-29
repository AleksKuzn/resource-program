import sys
import psycopg2
import KPU_ui, add_KPU_ui, replace_KPU_ui, pu   
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QTableWidgetItem
        
class Kpu(QtWidgets.QWidget, KPU_ui.Ui_Form):
    def __init__(self, conn, id_entr):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('КПУ')
        self.conn = conn 
        self.pushButton_add.clicked.connect(self.add_window)       
        cur = conn.cursor()
        cur.execute("""SELECT adress, id_kpu, id_entr, type_kpu, ser_num 
                       FROM cnt.kpu""") 
        data = cur.fetchall()
        for index,row in enumerate(data):
            self.tableWidget_kpu.insertRow(0)
            for k in range(len(row)):
                item = QTableWidgetItem(str(data[index][k]))
                self.tableWidget_kpu.setItem(0,k,item) 
        cur.close()        
        self.show()

    def add_window(self):
        self.add_kpu = add_Kpu()

    def cell_was_clicked(self, coords):
        id_scaut=self.tableWidget_kpu.item(coords.row(), 4).text()
        self.add_scaut = add_Scaut(id_scaut, self.conn)
        
class add_Kpu(QtWidgets.QWidget, add_KPU_ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Добавить КПУ')
        self.show()
        self.pushButton_pu.clicked.connect(self.open_pu)
        self.pushButton_replace.clicked.connect(self.replace)
        self.pushButton_save.clicked.connect(self.save)

    def save(self):
        self.close()

    def open_pu(self):
        self.pu = pu.Pu()
        #self.close()

    def replace(self):
        self.replace_kpu = replace_Kpu()
        #self.close()
        
class replace_Kpu(QtWidgets.QWidget, replace_KPU_ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Замена КПУ')
        self.show()
        self.pushButton_replace.clicked.connect(self.replace)
        self.pushButton_cansel.clicked.connect(self.cansel)

    def cansel(self):
        self.close()

    def replace(self):
        self.close()


