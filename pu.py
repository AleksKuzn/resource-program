import sys
import psycopg2
import datetime
import PU_ui, add_PU_ui, KPU_ui    
from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtWidgets import  QTableWidgetItem, QCheckBox
#from PyQt5.QtGui import *
from PyQt5.Qt import *
from datetime import timedelta 
       
class Pu(QtWidgets.QWidget, PU_ui.Ui_Form):
    def __init__(self, conn, id_kpu):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('ПУ')
        self.id_kpu=id_kpu
        self.conn = conn
        self.pushButton_add.clicked.connect(self.add_window)
        self.tableWidget_pu.doubleClicked.connect(self.cell_was_clicked)
        self.select()     
        self.pushButton_filtr.clicked.connect(self.select)
        self.tableWidget_pu.horizontalHeader().hideSection(0)
        self.tableWidget_pu.horizontalHeader().hideSection(16)
        self.filtr_city()
        self.comboBox_city.currentIndexChanged.connect(self.filtr_street)
        #self.comboBox_city.setCurrentText('Обнинск')
        #self.comboBox_street.currentIndexChanged.connect(self.filtr_house)
        #self.comboBox_house.currentIndexChanged.connect(self.filtr_entrance)
        #self.comboBox_house.currentIndexChanged.connect(self.filtr_flat)
        if (self.id_kpu!='-1') and (self.tableWidget_pu.rowCount() > 0): 
            self.comboBox_city.setCurrentText(self.tableWidget_pu.item(0,1).text())
            self.filtr_street()
            self.comboBox_street.setCurrentText(self.tableWidget_pu.item(0,2).text())
            self.comboBox_house.setCurrentText(self.tableWidget_pu.item(0,3).text())
            self.comboBox_entr.setCurrentText(self.tableWidget_pu.item(0,4).text())
        self.filtr_serKpu()
        self.show() 
    
    def filtr_city(self):
        self.comboBox_city.clear()        
        self.comboBox_city.id = []       
        self.comboBox_city.addItem('')
        cur = self.conn.cursor()
        city_query = """SELECT DISTINCT
                            city.city_name,	
                            city.id_city 
                        FROM
                            public.flat
                            inner join cnt.counter
                                on counter.id_flat=flat.id_flat
                            inner join cnt.kpu
                                on kpu.id_kpu = counter.id_kpu
                            inner join public.entrance
                                on entrance.id_entr = kpu.id_entr
                            left join public.house
                                on house.id_house = entrance.id_house
                            left join public.street
                                on street.id_street = house.id_street
                            left join public.city
                                on city.id_city = street.id_city
                        order by city.city_name"""                                                      
        cur.execute(city_query)        
        data = cur.fetchall()
        self.list_id_city = [0]
        for index,row in enumerate(data):           
            self.list_id_city.append(data[index][1])
            self.comboBox_city.addItem(str(data[index][0]))
        cur.close()   
        
    def filtr_street(self):   
        self.comboBox_street.clear()        
        self.comboBox_street.id = []        
        self.comboBox_street.addItem('')
        cur = self.conn.cursor() 
        # street_query = """SELECT
                            # street.street_name,	
                            # street.id_street                             
                        # FROM
                            # public.street""" 

        street_query = """SELECT DISTINCT
                            street.street_name,	
                            street.id_street 
                        FROM
                            public.flat
                            inner join cnt.counter
                                on counter.id_flat=flat.id_flat
                            inner join cnt.kpu
                                on kpu.id_kpu = counter.id_kpu
                            inner join public.entrance
                                on entrance.id_entr = kpu.id_entr
                            left join public.house
                                on house.id_house = entrance.id_house
                            left join public.street
                                on street.id_street = house.id_street"""                    
        street_query = street_query + " WHERE street.id_city = " + str(self.list_id_city[self.comboBox_city.currentIndex()]) + " order by street.street_name"                      
        cur.execute(street_query)        
        data = cur.fetchall()
        self.list_id_street = [0]
        for index,row in enumerate(data):   
            self.list_id_street.append(data[index][1])
            self.comboBox_street.addItem(str(data[index][0]))    
        cur.close()
        self.comboBox_street.currentIndexChanged.connect(self.filtr_house)
        
    def filtr_house(self):
        self.comboBox_house.clear()        
        self.comboBox_house.id = []        
        self.comboBox_house.addItem('')
        cur = self.conn.cursor()
        # house_query = """SELECT
                            # house.house_number,	
                            # house.id_house                             
                        # FROM
                            # public.house""" 
        house_query = """SELECT DISTINCT
                            house.house_number,	
                            house.id_house 
                        FROM
                            public.flat
                            inner join cnt.counter
                                on counter.id_flat=flat.id_flat
                            inner join cnt.kpu
                                on kpu.id_kpu = counter.id_kpu
                            inner join public.entrance
                                on entrance.id_entr = kpu.id_entr
                            left join public.house
                                on house.id_house = entrance.id_house"""
        #house_query = house_query + " WHERE house.id_street = " + str(self.list_id_street[self.comboBox_street.currentIndex()]) + " order by street.street_name"       
        house_query = house_query + " WHERE house.id_street = " + str(self.list_id_street[self.comboBox_street.currentIndex()]) + " order by house.house_number"       
        cur.execute(house_query)   
        data = cur.fetchall()
        self.list_id_house = [0]
        for index,row in enumerate(data):  
            self.list_id_house.append(data[index][1])  
            self.comboBox_house.addItem(str(data[index][0]))          
        cur.close()
        self.comboBox_house.currentIndexChanged.connect(self.filtr_entrance)
        
    def filtr_entrance(self):
        self.comboBox_entr.clear()        
        self.comboBox_entr.id = []        
        self.comboBox_entr.addItem('')
        cur = self.conn.cursor()
        entrance_query = """SELECT
                            entrance.num_entr,	
                            entrance.id_entr                             
                        FROM
                            public.entrance"""                            
        entrance_query = entrance_query + " WHERE entrance.id_house = " + str(self.list_id_house[self.comboBox_house.currentIndex()]) + " order by cast(entrance.num_entr as integer)"
        cur.execute(entrance_query) 
        data = cur.fetchall()
        self.list_id_entrance = [0]
        for index,row in enumerate(data):
            self.list_id_entrance.append(data[index][1])        
            self.comboBox_entr.addItem(str(data[index][0]))        
        cur.close()
            #self.id_kpu='-1'       
        self.filtr_flat()
        self.comboBox_entr.currentIndexChanged.connect(self.filtr_floor)
        #self.comboBox_entr.currentIndexChanged.connect(self.filtr_flat)
        
    def filtr_floor(self):
        self.comboBox_floor.clear()        
        self.comboBox_floor.id = []        
        self.comboBox_floor.addItem('')
        cur = self.conn.cursor()
        entrance_query = """SELECT DISTINCT
                            flat.flatfloor                            
                        FROM
                            public.flat"""                                
        entrance_query = entrance_query + " WHERE flat.id_entr = " + str(self.list_id_entrance[self.comboBox_entr.currentIndex()]) + " order by cast(flat.flatfloor as integer)"
        cur.execute(entrance_query) 
        data = cur.fetchall()
        for index,row in enumerate(data):       
            self.comboBox_floor.addItem(str(data[index][0]))        
        cur.close()
        self.filtr_flat()
        self.comboBox_floor.currentIndexChanged.connect(self.filtr_flat)
        
    def filtr_flat(self):
        self.comboBox_flat.clear()        
        self.comboBox_flat.id = []        
        self.comboBox_flat.addItem('')
        cur = self.conn.cursor()
        entrance_query = """SELECT
                            flat.num_flat,
                            flat.id_flat
                        FROM
                            public.flat"""               
        if (self.comboBox_entr.currentText() == ''): 
            id_house = self.list_id_house[self.comboBox_house.currentIndex()]
            entrance_query = entrance_query + " WHERE flat.id_entr in (SELECT entrance.id_entr FROM public.entrance WHERE entrance.id_house = " + str(id_house) +")" 
        else: 
            entrance_query = entrance_query + " WHERE flat.id_entr = " + str(self.list_id_entrance[self.comboBox_entr.currentIndex()]) 
        if (self.comboBox_floor.currentText() != ''): 
            entrance_query = entrance_query + "AND flat.flatfloor = " + (self.comboBox_floor.currentText())
        entrance_query = entrance_query + " order by cast(flat.num_flat as integer)"
        cur.execute(entrance_query) 
        data = cur.fetchall()
        self.list_id_flat = [0]
        for index,row in enumerate(data):       
            self.list_id_flat.append(data[index][1])
            self.comboBox_flat.addItem(str(data[index][0]))        
        cur.close()
        self.filtr_serKpu()
        self.comboBox_flat.currentIndexChanged.connect(self.filtr_serKpu)
        
    def filtr_serKpu(self):
        self.comboBox_serKpu.clear()        
        self.comboBox_serKpu.id = []        
        self.comboBox_serKpu.addItem('')
        cur = self.conn.cursor()
        entrance_query = """SELECT DISTINCT
                            kpu.ser_num, kpu.id_kpu                           
                        FROM
                            cnt.kpu  
                              left join public.entrance
                                on entrance.id_entr = kpu.id_entr
                              inner join public.flat
                                on flat.id_entr = kpu.id_entr
                              left join public.house
                                on house.id_house = entrance.id_house
                              left join public.street
                                on street.id_street = house.id_street
                              left join public.city
                                on city.id_city = street.id_city"""                                
        
        if self.id_kpu!='-1':
            self.sql_query = self.sql_query + " WHERE kpu.id_kpu = " + str(self.id_kpu)
        if self.id_kpu=='-1':
            if self.comboBox_city.currentText()!='':
                if self.comboBox_street.currentText()!='':
                    if self.comboBox_house.currentText()!='':
                        if self.comboBox_entr.currentText()!='':
                            if self.comboBox_floor.currentText()!='':
                                if self.comboBox_flat.currentText()!='':
                                    self.sql_query = self.sql_query + " WHERE flat.id_flat = " + str(self.list_id_flat[self.comboBox_flat.currentIndex()])
                                else: 
                                    self.sql_query = self.sql_query + " WHERE flat.flatfloor = " + str(self.comboBox_floor.currentIndex())
                            else:
                                self.sql_query = self.sql_query + " WHERE entrance.id_entr = " + str(self.list_id_entrance[self.comboBox_entr.currentIndex()])
                        else: 
                            self.sql_query = self.sql_query + " WHERE house.id_house = " + str(self.list_id_house[self.comboBox_house.currentIndex()])
                    else:
                        self.sql_query = self.sql_query + " WHERE street.id_street = " + str(self.list_id_street[self.comboBox_street.currentIndex()]) 
                else:
                    self.sql_query = self.sql_query + " WHERE city.id_city = " + str(self.list_id_city[self.comboBox_city.currentIndex()])         
            else:
                self.sql_query = self.sql_query + " ORDER BY kpu.ser_num DESC" 
        cur.execute(entrance_query)
        data = cur.fetchall()
        self.list_id_kpu = [0]
        for index,row in enumerate(data):
            self.list_id_kpu.append(data[index][1])
            self.comboBox_serKpu.addItem(str(data[index][0])) 
        cur.close()
        if (self.id_kpu!='-1') and (self.tableWidget_pu.rowCount() > 0):
            self.comboBox_serKpu.setCurrentText(self.tableWidget_pu.item(0,9).text())
            #self.id_kpu='-1'
        
    def select(self):
        self.tableWidget_pu.setRowCount(0)     
        self.sql_query = """SELECT  			 			
                              counter.id_klemma, city.city_name,
                              street.street_name, house.house_number,
                              entrance.num_entr, flat.flatfloor, flat.num_flat,
                              case counter.type_counter 		
                                when 1 then 'ГВС'
                                when 2 then 'ХВС'
                                when 3 then 'Т'
                                when 4 then 'Э' 
                              end AS Тип, counter.serial_number,		
                              kpu.ser_num, counter.klemma,			
                              marka.name_marka, counter.coefficient, 
                              counter.last_pok, counter.date_install,
                              counter.date_deinstall, counter.working_capacity
                            FROM
                              cnt.counter
                              left join public.flat
                                on flat.id_flat = counter.id_flat
                              inner join cnt.kpu
                                on counter.id_kpu=kpu.id_kpu
                              inner join cnt.marka
                                on counter.id_marka = marka.id_marka
                              left join public.entrance
                                on entrance.id_entr = flat.id_entr
                              inner join public.house
                                on house.id_house = entrance.id_house
                              inner join public.street
                                on street.id_street = house.id_street
                              inner join public.city
                                on city.id_city = street.id_city"""
        if self.id_kpu!='-1':
            self.sql_query = self.sql_query + " WHERE kpu.id_kpu = " + str(self.id_kpu)
            self.tableWidget_pu.horizontalHeader().hideSection(1)
            self.tableWidget_pu.horizontalHeader().hideSection(2)
            self.tableWidget_pu.horizontalHeader().hideSection(3)
            self.tableWidget_pu.horizontalHeader().hideSection(4)
        if self.id_kpu=='-1':
            if self.comboBox_city.currentText()!='':
                self.tableWidget_pu.horizontalHeader().hideSection(1)
                if self.comboBox_street.currentText()!='':
                    self.tableWidget_pu.horizontalHeader().hideSection(2)
                    if self.comboBox_house.currentText()!='':
                        self.tableWidget_pu.horizontalHeader().hideSection(3)
                        if self.comboBox_entr.currentText()!='':
                            self.tableWidget_pu.horizontalHeader().hideSection(4)
                            self.sql_query = self.sql_query + " WHERE entrance.id_entr = " + str(self.list_id_entrance[self.comboBox_entr.currentIndex()])
                        else: 
                            self.tableWidget_pu.horizontalHeader().showSection(4)
                            self.sql_query = self.sql_query + " WHERE house.id_house = " + str(self.list_id_house[self.comboBox_house.currentIndex()])
                    else:
                        self.tableWidget_pu.horizontalHeader().showSection(4)
                        self.tableWidget_pu.horizontalHeader().showSection(3)
                        self.sql_query = self.sql_query + " WHERE street.id_street = " + str(self.list_id_street[self.comboBox_street.currentIndex()]) 
                else:
                    self.tableWidget_pu.horizontalHeader().showSection(4)
                    self.tableWidget_pu.horizontalHeader().showSection(3)
                    self.tableWidget_pu.horizontalHeader().showSection(2)
                    self.sql_query = self.sql_query + " WHERE city.id_city = " + str(self.list_id_city[self.comboBox_city.currentIndex()])         
            else:
                self.tableWidget_pu.horizontalHeader().showSection(4)
                self.tableWidget_pu.horizontalHeader().showSection(3)
                self.tableWidget_pu.horizontalHeader().showSection(2)
                self.tableWidget_pu.horizontalHeader().showSection(1)
        self.sql_query = self.sql_query + " ORDER BY city.city_name, street.street_name, cast(substring(house.house_number from '^[0-9]+') as integer), cast(entrance.num_entr as integer), flat.num_flat, counter.type_counter DESC"     
        cur = self.conn.cursor()
        cur.execute(self.sql_query)  
        data = cur.fetchall()
        for index,row in enumerate(data):
            self.tableWidget_pu.insertRow(0)
            for k in range(len(row)):
                    item = QTableWidgetItem('' if data[index][k]==None else str(data[index][k]))                 
                    self.tableWidget_pu.setItem(0,k,item)
                    if data[index][16]==False:
                        self.tableWidget_pu.item(0, k).setBackground(QtGui.QColor(245,245,245))
                        self.tableWidget_pu.item(0, k).setForeground(QtGui.QColor(110,110,110))             
        cur.close()   
        self.tableWidget_pu.resizeColumnsToContents()
        self.tableWidget_pu.setMouseTracking(True)
        self.current_hover = 0
        self.tableWidget_pu.cellEntered.connect(self.line_selection)
    
    def line_selection(self, row, column):
        if self.current_hover != row:
            for j in range(self.tableWidget_pu.columnCount()):
                if self.tableWidget_pu.item(self.current_hover,16).text()=='False':        
                    self.tableWidget_pu.item(self.current_hover, j).setBackground(QtGui.QColor(245,245,245))                   
                else:
                    self.tableWidget_pu.item(self.current_hover, j).setBackground(QBrush(QColor('white')))
                self.tableWidget_pu.item(row, j).setBackground(QBrush(QColor('lightGray')))
        self.current_hover = row
        
    def add_window(self):
        self.add_pu = add_Pu('-1', self.conn)
        
    def cell_was_clicked(self, coords):
        id_pu=self.tableWidget_pu.item(coords.row(), 0).text()
        self.add_pu=add_Pu(id_pu, self.conn)

class add_Pu(QtWidgets.QWidget, add_PU_ui.Ui_Form):
    def __init__(self, id_pu, conn):
        super().__init__()
        self.setupUi(self)
        self.conn = conn
        self.id_pu = id_pu
        
        self.pushButton_addStart.clicked.connect(self.add_start)
        self.pushButton_save.clicked.connect(self.save)
        self.pushButton_replace.clicked.connect(self.replace)
        
        if self.id_pu=='-1':
            self.setWindowTitle('Добавить ПУ')
        if self.id_pu!='-1':
            self.setWindowTitle('Изменить информацию о ПУ')
        self.show()
    def save(self):
        self.close()

    def add_start(self):
        self.close()
        
    def replace(self):
        pass
