import sys
import psycopg2
import KPU_ui, add_KPU_ui, replace_KPU_ui, pu   
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QTableWidgetItem
from PyQt5.QtGui import *
#from PyQt5.QtCore import *
        
class Kpu(QtWidgets.QWidget, KPU_ui.Ui_Form):
    def __init__(self, conn, id_entr):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('КПУ')
        self.id_entr=id_entr
        self.conn = conn 
        self.pushButton_add.clicked.connect(self.add_window)
        self.tableWidget_kpu.doubleClicked.connect(self.cell_was_clicked)        
        self.scaut_query()
        self.filtr_city()
        self.pushButton_filtr.clicked.connect(self.scaut_query)
        self.tableWidget_kpu.horizontalHeader().hideSection(0)       
        self.show()
    
    def filtr_city(self):
        self.comboBox_city.clear()        
        self.comboBox_city.id = []       
        self.comboBox_city.addItem('')
        cur = self.conn.cursor()
        city_query = """SELECT
                            city.city_name,	
                            city.id_city                             
                        FROM
                            public.city
                        order by city.city_name;"""                                                      
        cur.execute(city_query)        
        data = cur.fetchall()
        self.list_id_city = [0]
        for index,row in enumerate(data):           
            self.list_id_city.append(data[index][1])
            self.comboBox_city.addItem(str(data[index][0]))
        cur.close()
        self.comboBox_city.setCurrentText('Обнинск')
        self.filtr_street()
        self.comboBox_city.currentIndexChanged.connect(self.filtr_street)      
        
    def filtr_street(self):     
        self.comboBox_street.clear()        
        self.comboBox_street.id = []        
        self.comboBox_street.addItem('')
        cur = self.conn.cursor() 
        street_query = """SELECT
                            street.street_name,	
                            street.id_street                             
                        FROM
                            public.street"""                     
        street_query = street_query + " WHERE street.id_city = " + str(self.list_id_city[self.comboBox_city.currentIndex()]) + " order by street.street_name"                      
        cur.execute(street_query)        
        data = cur.fetchall()
        self.list_id_street = [0]
        for index,row in enumerate(data):   
            self.list_id_street.append(data[index][1])
            self.comboBox_street.addItem(str(data[index][0]))    
        cur.close()      
        self.comboBox_street.setCurrentText('Поленова')
        self.filtr_house()
        self.comboBox_street.currentIndexChanged.connect(self.filtr_house)
        
    def filtr_house(self):
        self.comboBox_house.clear()        
        self.comboBox_house.id = []        
        self.comboBox_house.addItem('')
        cur = self.conn.cursor()
        house_query = """SELECT
                            house.house_number,	
                            house.id_house                             
                        FROM
                            public.house"""                    
        house_query = house_query + " WHERE house.id_street = " + str(self.list_id_street[self.comboBox_street.currentIndex()]) + " order by cast(substring(house.house_number from \'^[0-9]+\') as integer)"       
        cur.execute(house_query)         
        data = cur.fetchall()
        self.list_id_house = [0]
        for index,row in enumerate(data):  
            self.list_id_house.append(data[index][1])  
            self.comboBox_house.addItem(str(data[index][0]))          
        cur.close()
        self.comboBox_house.currentIndexChanged.connect(self.filtr_entrance)
        
    def filtr_entrance(self):
        self.comboBox_entrance.clear()        
        self.comboBox_entrance.id = []        
        self.comboBox_entrance.addItem('')
        cur = self.conn.cursor()
        entrance_query = """SELECT
                            entrance.num_entr,	
                            entrance.id_entr                             
                        FROM
                            public.entrance"""                                
        entrance_query = entrance_query + " WHERE entrance.id_house = " + str(self.list_id_house[self.comboBox_house.currentIndex()]) + " order by cast(entrance.num_entr as integer)"
        cur.execute(entrance_query) 
        data = cur.fetchall()
        self.list_id_entrace = [0]
        for index,row in enumerate(data):
            self.list_id_entrace.append(data[index][1])        
            self.comboBox_entrance.addItem(str(data[index][0]))        
        cur.close()
    
    def scaut_query(self):
        self.tableWidget_kpu.setRowCount(0)
        
        self.sql_query = """SELECT  
                              kpu.id_kpu,
                              city.city_name, street.street_name,
                              house.house_number, entrance.num_entr,
                              kpu.ser_num, kpu.adress,
                              kpu.type_kpu, kpu.floor,
                              kpu.note, kpu.workability	                            
                            FROM
                              cnt.kpu  
                              inner join public.entrance
                                on entrance.id_entr = kpu.id_entr
                              inner join public.house
                                on house.id_house = entrance.id_house
                              inner join public.street
                                on street.id_street = house.id_street
                              inner join public.city
                                on city.id_city = street.id_city"""
        if self.id_entr!='-1':
            self.sql_query = self.sql_query + ' WHERE kpu.id_entr = ' + self.id_entr
        self.sql_query = self.sql_query + ' ORDER BY city.city_name, street.street_name, cast(substring(house.house_number from \'^[0-9]+\') as integer), cast(entrance.num_entr as integer), kpu.type_kpu, kpu.adress DESC'     
        cur = self.conn.cursor()
        cur.execute(self.sql_query)   
        data = cur.fetchall()
        for index,row in enumerate(data):
            self.tableWidget_kpu.insertRow(0)
            for k in range(len(row)):
                if str(data[index][k])!='': #нужно исправить, это не работает
                    item = QTableWidgetItem(str(data[index][k]))
                    self.tableWidget_kpu.setItem(0,k,item)        
        cur.close()
        self.tableWidget_kpu.setMouseTracking(True)
        self.current_hover = 0
        self.tableWidget_kpu.cellEntered.connect(self.line_selection)
    
    def line_selection(self, row, column):
        if self.current_hover != row:
            for j in range(self.tableWidget_kpu.columnCount()):
                self.tableWidget_kpu.item(self.current_hover, j).setBackground(QBrush(QColor('white')))
                self.tableWidget_kpu.item(row, j).setBackground(QBrush(QColor('lightGray')))
        self.current_hover = row
    
    def add_window(self):
        self.add_kpu = add_Kpu('-1', self.conn)

    def cell_was_clicked(self, coords):
        id_kpu=self.tableWidget_kpu.item(coords.row(), 0).text()
        self.add_kpu = add_Kpu(id_kpu, self.conn)
        
class add_Kpu(QtWidgets.QWidget, add_KPU_ui.Ui_Form):
    def __init__(self, id_kpu, conn):
        super().__init__()
        self.setupUi(self)
        self.id_kpu = id_kpu 
        self.label_error.hide()
        self.conn = conn 
        self.filtr_city()       
        cur = self.conn.cursor()
        if self.id_kpu=='-1':
            self.setWindowTitle('Добавить КПУ')
            self.pushButton_pu.hide()
            self.pushButton_save.clicked.connect(self.insert)
            self.comboBox_city.setCurrentText('Обнинск')
            self.comboBox_street.setCurrentText('Поленова')
        if self.id_kpu!='-1':      
            self.setWindowTitle('информация КПУ')
            self.pushButton_pu.show()            
            self.pushButton_pu.clicked.connect(self.open_pu)
            self.pushButton_replace.clicked.connect(self.replace)
            self.pushButton_save.clicked.connect(self.update)
        self.show()
    
    def update(self):
        self.close()
    
    def insert(self):
        if self.comboBox_house.currentText()!='' and self.lineEdit_entrance.text()!='':           
            # print(self.list_id_house[self.comboBox_house.currentIndex()])
            # print(self.lineEdit_entrance.text())
            # print(self.lineEdit_host.text())
            # print(self.lineEdit_port.text())
            # print(self.lineEdit_login.text())
            # print(self.lineEdit_pasw.text())
            cur = self.conn.cursor()
            sql_query = """INSERT INTO count.kpu(id_house, num_entr, ip_rassbery, 
                                                port_rassbery, login_user, pwd_user)                                                                                             
                        VALUES (%s, %s, %s, %s, %s, %s)"""
            cur.execute(sql_query, (str(self.list_id_house[self.comboBox_house.currentIndex()]), str(self.lineEdit_entrance.text()), str(self.lineEdit_host.text()), str(self.lineEdit_port.text()), str(self.lineEdit_login.text()), str(self.lineEdit_pasw.text())))        

            cur.close()                
#           self.conn.commit()
            self.close()
        else:         
            pal = self.label_error.palette()
            pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
            self.label_error.setPalette(pal)
            self.label_error.setText("Укажите номер дома и подъезда")
#            self.resize(self.label_error.sizeHint())         
            self.label_error.show()

    def open_pu(self):
        self.pu = pu.Pu()
        #self.close()

    def replace(self):
        self.replace_kpu = replace_Kpu()
        #self.close()
    
    def filtr_city(self):
        self.comboBox_city.clear()        
        self.comboBox_city.id = []
        self.comboBox_city.addItem('')        
        cur = self.conn.cursor()
        city_query = """SELECT
                            city.city_name,	
                            city.id_city                             
                        FROM
                            public.city
                        order by city.city_name;"""                                                      
        cur.execute(city_query)  
        data = cur.fetchall()
        self.list_id_city = [0]
        for index,row in enumerate(data):           
            self.list_id_city.append(data[index][1])
            self.comboBox_city.addItem(str(data[index][0]))
        cur.close()
        self.filtr_street()
        self.comboBox_city.currentIndexChanged.connect(self.filtr_street)      
        
    def filtr_street(self):     
        self.comboBox_street.clear()        
        self.comboBox_street.id = []        
        self.comboBox_street.addItem('')      
        cur = self.conn.cursor() 
        street_query = """SELECT
                            street.street_name,	
                            street.id_street                             
                        FROM
                            public.street"""                     
        street_query = street_query + " WHERE street.id_city = " + str(self.list_id_city[self.comboBox_city.currentIndex()]) + " order by street.street_name"                      
        cur.execute(street_query)        
        data = cur.fetchall()
        self.list_id_street = [0]
        for index,row in enumerate(data):   
            self.list_id_street.append(data[index][1])
            self.comboBox_street.addItem(str(data[index][0]))    
        cur.close()      
        self.filtr_house()
        self.comboBox_street.currentIndexChanged.connect(self.filtr_house)
        
    def filtr_house(self):    
        self.comboBox_house.clear()        
        self.comboBox_house.id = []        
        self.comboBox_house.addItem('')
        cur = self.conn.cursor()        
        house_query = """SELECT
                            house.house_number,	
                            house.id_house                             
                        FROM
                            public.house"""                                    
        house_query = house_query + " WHERE house.id_street = " + str(self.list_id_street[self.comboBox_street.currentIndex()]) + " order by cast(substring(house.house_number from \'^[0-9]+\') as integer)"       
        cur.execute(house_query)         
        data = cur.fetchall()
        self.list_id_house = [0]
        for index,row in enumerate(data):  
            self.list_id_house.append(data[index][1])  
            self.comboBox_house.addItem(str(data[index][0]))  
        cur.close()
        self.filtr_entrance()
        self.comboBox_house.currentIndexChanged.connect(self.filtr_entrance)
    
    def filtr_entrance(self):
        self.comboBox_entrance.clear() 
        self.comboBox_entrance.id = []        
        self.comboBox_entrance.addItem('')
        cur = self.conn.cursor()
        entrance_query = """SELECT
                            entrance.num_entr,	
                            entrance.id_entr                             
                        FROM
                            public.entrance"""                                
        entrance_query = entrance_query + " WHERE entrance.id_house = " + str(self.list_id_house[self.comboBox_house.currentIndex()]) + " order by cast(entrance.num_entr as integer)"
        cur.execute(entrance_query) 
        data = cur.fetchall()
        self.list_id_entrace = [0]
        for index,row in enumerate(data):
            self.list_id_entrace.append(data[index][1])        
            self.comboBox_entrance.addItem(str(data[index][0]))        
        cur.close()
        
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


