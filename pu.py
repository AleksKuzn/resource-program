import sys
import psycopg2
import datetime
import PU_ui, add_PU_ui, info_PU_ui, KPU_ui    
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
        self.tableWidget_pu.horizontalHeader().hideSection(17)
        self.checkBox_true.stateChanged.connect(self.workT)
        self.checkBox_false.stateChanged.connect(self.workF)
        self.filtr()
        self.show() 
        
    def workT(self):
        if not (self.checkBox_true.isChecked()) and not (self.checkBox_false.isChecked()):
            self.checkBox_true.setChecked(False) 
            self.checkBox_false.setChecked(True)
            
    def workF(self):
        if not (self.checkBox_true.isChecked()) and not (self.checkBox_false.isChecked()):
            self.checkBox_true.setChecked(True) 
            self.checkBox_false.setChecked(False)
        
    def filtr(self):
            self.filtr_city()
            self.filtr_serKpu()
            if (self.id_kpu!='-1') and (self.tableWidget_pu.rowCount() > 0):
                self.comboBox_serKpu.setCurrentText(self.tableWidget_pu.item(0,9).text())
            self.comboBox_city.currentIndexChanged.connect(self.filtr_street)
            if (self.id_kpu!='-1') and (self.tableWidget_pu.rowCount() > 0):
                self.comboBox_city.setCurrentText(self.tableWidget_pu.item(0,1).text())
            self.comboBox_street.currentIndexChanged.connect(self.filtr_house)
            if (self.id_kpu!='-1') and (self.tableWidget_pu.rowCount() > 0):
                self.comboBox_street.setCurrentText(self.tableWidget_pu.item(0,2).text())
            self.comboBox_house.currentIndexChanged.connect(self.filtr_entrance)
            if (self.id_kpu!='-1') and (self.tableWidget_pu.rowCount() > 0):
                self.comboBox_house.setCurrentText(self.tableWidget_pu.item(0,3).text())
            self.comboBox_entr.currentIndexChanged.connect(self.filtr_floor)
            if (self.id_kpu!='-1') and (self.tableWidget_pu.rowCount() > 0):
                self.comboBox_entr.setCurrentText(self.tableWidget_pu.item(0,4).text())
            self.comboBox_floor.currentIndexChanged.connect(self.filtr_flat)
            self.comboBox_flat.currentIndexChanged.connect(self.filtr_serKpu)
            self.id_kpu='-1'
            
    def filtr_city(self):
        self.comboBox_city.clear()        
        self.comboBox_city.id = []
        self.list_id_city = [0]
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
        for index,row in enumerate(data):           
            self.list_id_city.append(data[index][1])
            self.comboBox_city.addItem(str(data[index][0]))
        cur.close()
        
    def filtr_street(self):  
        self.comboBox_street.clear()        
        self.comboBox_street.id = []
        self.list_id_street = [0]
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
        for index,row in enumerate(data):   
            self.list_id_street.append(data[index][1])
            self.comboBox_street.addItem(str(data[index][0]))    
        cur.close()
        
    def filtr_house(self):
        self.comboBox_house.clear()        
        self.comboBox_house.id = []
        self.list_id_house = [0]
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
        for index,row in enumerate(data):  
            self.list_id_house.append(data[index][1])  
            self.comboBox_house.addItem(str(data[index][0]))          
        cur.close()
        
    def filtr_entrance(self):
        self.comboBox_entr.clear()        
        self.comboBox_entr.id = [] 
        self.list_id_entrance = [0]
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
        for index,row in enumerate(data):
            self.list_id_entrance.append(data[index][1])        
            self.comboBox_entr.addItem(str(data[index][0]))        
        cur.close()
        
    def filtr_floor(self):
        self.comboBox_floor.clear()        
        self.comboBox_floor.id = []        
        self.comboBox_floor.addItem('')
        cur = self.conn.cursor()
        floor_query = """SELECT DISTINCT
                            flat.flatfloor                            
                        FROM
                            public.flat"""                                
        floor_query = floor_query + " WHERE flat.id_entr = " + str(self.list_id_entrance[self.comboBox_entr.currentIndex()]) + " order by cast(flat.flatfloor as integer)"
        cur.execute(floor_query) 
        data = cur.fetchall()
        for index,row in enumerate(data):       
            self.comboBox_floor.addItem(str(data[index][0]))        
        cur.close()
        
    def filtr_flat(self):
        self.comboBox_flat.clear()        
        self.comboBox_flat.id = []  
        self.list_id_flat = [0]
        self.comboBox_flat.addItem('')
        cur = self.conn.cursor()
        flat_query = """SELECT
                            flat.num_flat,
                            flat.id_flat
                        FROM
                            public.flat"""               
        if (self.comboBox_entr.currentText() == ''): 
            id_house = self.list_id_house[self.comboBox_house.currentIndex()]
            flat_query = flat_query + " WHERE flat.id_entr in (SELECT entrance.id_entr FROM public.entrance WHERE entrance.id_house = " + str(id_house) +")" 
        else: 
            flat_query = flat_query + " WHERE flat.id_entr = " + str(self.list_id_entrance[self.comboBox_entr.currentIndex()]) 
        if (self.comboBox_floor.currentText() != ''): 
            flat_query = flat_query + "AND flat.flatfloor = " + (self.comboBox_floor.currentText())
        flat_query = flat_query + " order by cast(flat.num_flat as integer)"
        cur.execute(flat_query) 
        data = cur.fetchall()
        for index,row in enumerate(data):       
            self.list_id_flat.append(data[index][1])
            self.comboBox_flat.addItem(str(data[index][0]))        
        cur.close()
        
    def filtr_serKpu(self):
        self.comboBox_serKpu.clear()        
        self.comboBox_serKpu.id = []
        self.list_id_kpu = [0]
        self.comboBox_serKpu.addItem('')
        cur = self.conn.cursor()
        kpu_query = """SELECT DISTINCT
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
        if self.comboBox_city.currentText()!='':
            if self.comboBox_street.currentText()!='':
                if self.comboBox_house.currentText()!='':
                    if self.comboBox_entr.currentText()!='':
                            kpu_query = kpu_query + " WHERE entrance.id_entr = " + str(self.list_id_entrance[self.comboBox_entr.currentIndex()])
                    else: 
                        kpu_query = kpu_query + " WHERE house.id_house = " + str(self.list_id_house[self.comboBox_house.currentIndex()])
                else:
                    kpu_query = kpu_query + " WHERE street.id_street = " + str(self.list_id_street[self.comboBox_street.currentIndex()]) 
            else:
                kpu_query = kpu_query + " WHERE city.id_city = " + str(self.list_id_city[self.comboBox_city.currentIndex()])         
        kpu_query = kpu_query + " ORDER BY kpu.ser_num DESC" 
        #print(kpu_query)
        cur.execute(kpu_query)
        data = cur.fetchall()
        for index,row in enumerate(data):
            self.list_id_kpu.append(data[index][1])
            self.comboBox_serKpu.addItem(str(data[index][0])) 
        cur.close()
    
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
                              kpu.ser_num, kpu.type_kpu, counter.klemma,
                              marka.name_marka, counter.coefficient, 
                              counter.last_pok, counter.date_install,
                              counter.date_deinstall, counter.working_capacity
                            FROM
                              cnt.counter
                              left join public.flat
                                on flat.id_flat = counter.id_flat
                              left join cnt.kpu
                                on counter.id_kpu=kpu.id_kpu
                              left join cnt.marka
                                on counter.id_marka = marka.id_marka
                              left join public.entrance
                                on entrance.id_entr = flat.id_entr
                              left join public.house
                                on house.id_house = entrance.id_house
                              left join public.street
                                on street.id_street = house.id_street
                              left join public.city
                                on city.id_city = street.id_city
                                WHERE counter.id_flat is not null"""
           
        if self.id_kpu!='-1':
            self.sql_query_where = " AND kpu.id_kpu = " + str(self.id_kpu)
            self.tableWidget_pu.horizontalHeader().hideSection(1)
            self.tableWidget_pu.horizontalHeader().hideSection(2)
            self.tableWidget_pu.horizontalHeader().hideSection(3)
            self.tableWidget_pu.horizontalHeader().hideSection(4)
        if self.id_kpu=='-1':
            self.sql_query_where = ''
            self.tableWidget_pu.horizontalHeader().showSection(5)
            self.tableWidget_pu.horizontalHeader().showSection(4)
            self.tableWidget_pu.horizontalHeader().showSection(3)
            self.tableWidget_pu.horizontalHeader().showSection(2)
            self.tableWidget_pu.horizontalHeader().showSection(1)
            if self.comboBox_city.currentText()!='':
                self.tableWidget_pu.horizontalHeader().hideSection(1)
                self.sql_query_where = self.sql_query_where + " AND city.id_city = " + str(self.list_id_city[self.comboBox_city.currentIndex()])
            if self.comboBox_street.currentText()!='':
                self.tableWidget_pu.horizontalHeader().hideSection(2)
                self.sql_query_where = self.sql_query_where + " AND street.id_street = " + str(self.list_id_street[self.comboBox_street.currentIndex()])
            if self.comboBox_house.currentText()!='':
                self.tableWidget_pu.horizontalHeader().hideSection(3)
                self.sql_query_where = self.sql_query_where + " AND house.id_house = " + str(self.list_id_house[self.comboBox_house.currentIndex()])
            if self.comboBox_entr.currentText()!='':
                self.tableWidget_pu.horizontalHeader().hideSection(4)
                self.sql_query_where = self.sql_query_where + " AND entrance.id_entr = " + str(self.list_id_entrance[self.comboBox_entr.currentIndex()])
            if self.comboBox_floor.currentText()!='' and self.comboBox_serKpu.currentText()=='':
                self.tableWidget_pu.horizontalHeader().hideSection(5)
                self.sql_query_where = self.sql_query_where + " AND flat.flatfloor = " + str(self.comboBox_floor.currentText())
            if self.comboBox_flat.currentText()!='' and self.comboBox_serKpu.currentText()=='':
                self.sql_query_where = self.sql_query_where + " AND flat.id_flat = " + str(self.list_id_flat[self.comboBox_flat.currentIndex()])
            if self.comboBox_serKpu.currentText()!='':
                self.sql_query_where = self.sql_query_where + " AND kpu.id_kpu = " + str(self.list_id_kpu[self.comboBox_serKpu.currentIndex()])
                ser_kpu = self.comboBox_serKpu.currentText()
                self.comboBox_floor.setCurrentText('')
                self.comboBox_flat.setCurrentText('')
                self.comboBox_serKpu.setCurrentText(ser_kpu)
            if self.comboBox_type.currentText()!='':
                self.sql_query_where = self.sql_query_where + " AND counter.type_counter = " + str(self.comboBox_type.currentIndex())
            if self.checkBox_true.isChecked() and not (self.checkBox_false.isChecked()):
                self.sql_query_where = self.sql_query_where + " AND counter.working_capacity = 'TRUE'"
            if self.checkBox_false.isChecked() and not (self.checkBox_true.isChecked()):
                self.sql_query_where = self.sql_query_where + " AND counter.working_capacity = 'FALSE'"
        self.sql_query = self.sql_query + self.sql_query_where
        self.sql_query = self.sql_query + """ UNION
                            SELECT
                                counter.id_klemma, city.city_name,
                                street.street_name, house.house_number,
                                entrance.num_entr, flat.flatfloor, flat.num_flat,
                                case counter.type_counter
                                when 1 then 'ГВС'
                                when 2 then 'ХВС'
                                when 3 then 'Т'
                                when 4 then 'Э' 
                                end AS Тип, counter.serial_number,
                                kpu.ser_num, kpu.type_kpu, counter.klemma,
                                marka.name_marka, counter.coefficient, 
                                counter.last_pok, counter.date_install,
                                counter.date_deinstall, counter.working_capacity
                            FROM
                                cnt.counter
                                inner join public.entrance
                                on entrance.id_entr = counter.id_entr
                                left join public.flat
                                on flat.id_flat = counter.id_flat
                                left join cnt.kpu
                                on counter.id_kpu=kpu.id_kpu
                                left join cnt.marka
                                on counter.id_marka = marka.id_marka
                                left join public.house
                                on house.id_house = entrance.id_house
                                left join public.street
                                on street.id_street = house.id_street
                                left join public.city
                                on city.id_city = street.id_city
                            WHERE counter.id_flat is null"""
        self.sql_query = self.sql_query + self.sql_query_where                    
        #self.sql_query = self.sql_query + " ORDER BY city.city_name, street.street_name, cast(substring(house.house_number from \'^[0-9]+\') as integer), cast(entrance.num_entr as integer), flat.num_flat, counter.type_counter DESC"     
        self.sql_query = self.sql_query + " ORDER BY 2 DESC, 3 DESC, 4 DESC, 5 DESC, 7 DESC, 8 DESC" 
        print(self.sql_query)
        cur = self.conn.cursor()
        cur.execute(self.sql_query)       
        data = cur.fetchall()
        cur.close() 
        for index,row in enumerate(data):
            self.tableWidget_pu.insertRow(0)
            for k in range(len(row)):
                    item = QTableWidgetItem('' if data[index][k]==None else str(data[index][k]))                 
                    self.tableWidget_pu.setItem(0,k,item)
                    if data[index][17]==False:
                        self.tableWidget_pu.item(0, k).setBackground(QtGui.QColor(245,245,245))
                        self.tableWidget_pu.item(0, k).setForeground(QtGui.QColor(110,110,110))   
        self.tableWidget_pu.resizeColumnsToContents()
        self.tableWidget_pu.setMouseTracking(True)
        self.current_hover = 0
        self.tableWidget_pu.cellEntered.connect(self.line_selection)
    
    def line_selection(self, row, column):
        if self.current_hover != row:
            for j in range(self.tableWidget_pu.columnCount()):
                if self.tableWidget_pu.item(self.current_hover,17).text()=='False':        
                    self.tableWidget_pu.item(self.current_hover, j).setBackground(QtGui.QColor(245,245,245))                   
                else:
                    self.tableWidget_pu.item(self.current_hover, j).setBackground(QBrush(QColor('white')))
                self.tableWidget_pu.item(row, j).setBackground(QBrush(QColor('lightGray')))
        self.current_hover = row
        
    def add_window(self):
        ser_num_kpu = self.comboBox_serKpu.currentText()
        city_name = self.comboBox_city.currentText()
        street_name = self.comboBox_street.currentText()
        house_number = self.comboBox_house.currentText()
        entrance_number = self.comboBox_entr.currentText()
        self.add_pu = Add_Pu(self.conn, ser_num_kpu, city_name, street_name, house_number, entrance_number)
        
    def cell_was_clicked(self, coords):
        id_pu=self.tableWidget_pu.item(coords.row(), 0).text()
        self.info_pu=Info_Pu(id_pu, self.conn)

class Add_Pu(QtWidgets.QWidget, add_PU_ui.Ui_Form):
    def __init__(self, conn, ser_num_kpu, city_name, street_name, house_number, entrance_number):
        super().__init__()
        self.setupUi(self)
        self.conn = conn
        self.ser_kpu = ser_num_kpu
        self.city = city_name
        self.street = street_name
        self.house = house_number
        self.entr = entrance_number
        self.widget_addFlat.hide()
        self.widget_stZn.hide()
        self.label_error.hide()
        self.checkBox_type.setChecked(False)
        self.label_entr.hide()
        self.comboBox_entr.hide()
        self.label_coefons.hide()
        self.lineEdit_coefons.hide()
        self.checkBox_type.stateChanged.connect(self.checkType)
        self.resize(500,300)
        self.lineEdit_serKpu.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.lineEdit_flat.setValidator(QRegExpValidator(QRegExp("[1-9][0-9]{,3}")))
        self.lineEdit_klemma.setValidator(QRegExpValidator(QRegExp("[1-9][0-9]")))
        self.pushButton_addStart.clicked.connect(self.insert_start_value)
        self.lineEdit_coefons.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.lineEdit_coef.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.lineEdit_floorAdd.setValidator(QRegExpValidator(QRegExp("[0-9][0-9]")))
        # self.lineEdit_pok.setValidator(QRegExpValidator(QRegExp("[0-9]{1,5}[\\.]{1,1}[0-9]{1,4}")))
        # self.lineEdit_imp.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.dateEdit_dateInstall.setDate(datetime.date.today())
        self.dateTimeEdit_date.setDateTime(datetime.datetime.today().replace(minute=0, second=0))
        self.filtr()
        self.pushButton_save.clicked.connect(self.verify)
        self.pushButton_cansel.clicked.connect(self.cansel)
        self.pushButton_addFlat.clicked.connect(self.insert_flat)
        self.setWindowTitle('Добавить квартирный ПУ')
        self.show()
    
    def checkType(self):
        if self.checkBox_type.isChecked():
            self.label_entr.show()
            self.comboBox_entr.show()
            self.label_coefons.show()
            self.lineEdit_coefons.show()
        else:
            self.label_entr.hide()
            self.comboBox_entr.hide()
            self.label_coefons.hide()
            self.lineEdit_coefons.hide() 

    def verify(self): #Доработать ошибки
        try:
            self.text='Введено некорректное значение'
            if self.lineEdit_serial.text()=='' and self.lineEdit_serKpu.text() == '': 
                self.text='Введите серийный номер счетчика или КПУ'
                raise ValueError
            if self.lineEdit_serial.text()=='' and self.lineEdit_klemma.text() == '': 
                self.text='Введите серийный номер счетчика или номер клеммы'
                raise ValueError    
            if self.comboBox_house.currentText() =='' and self.lineEdit_flat.text() !='':
                self.text='Укажите номер дома'
                raise ValueError
            self.val_serKpu = str(self.lineEdit_serKpu.text())
            self.val_serKpu = None if self.val_serKpu == '' else int(self.val_serKpu)
            self.val_house = str(self.comboBox_house.currentText())
            if self.val_house != '':
                self.val_id_house = int(self.list_id_house[self.comboBox_house.currentIndex()])
            else: self.val_id_house = None     
            self.val_entr = str(self.comboBox_entr.currentText())
            if self.val_entr != '':
                self.val_id_entr = int(self.list_id_entrance[self.comboBox_entr.currentIndex()])
            else: self.val_id_entr = None
            self.val_flat = str(self.lineEdit_flat.text())
            self.val_flat = None if self.val_flat == '' else int(self.val_flat)
            self.val_type = int(self.comboBox_type.currentIndex())
            if self.val_type == 0: self.val_type = None
            self.val_klemma = str(self.lineEdit_klemma.text())
            self.val_klemma = None if self.val_klemma == '' else int(self.val_klemma)
            self.val_serial = str(self.lineEdit_serial.text())
            if self.val_serial == '': self.val_serial = None
            self.val_coef = str(self.lineEdit_coef.text())
            self.val_coef = None if self.val_coef == '' else int(self.val_coef)
            self.val_coefons = str(self.lineEdit_coefons.text())
            self.val_coefons = 1 if self.val_coefons == '' else int(self.val_coefons)
            self.val_id_marka = int(self.list_id_marka[self.comboBox_marka.currentIndex()])
            if self.val_id_marka == 0: self.val_id_marka = None
            self.val_date = self.dateEdit_dateInstall.date().toString("yyyy-MM-dd")
            self.box_type = int(self.checkBox_type.isChecked())
            self.box_work = self.checkBox.isChecked()
            numberFlat = -1
            if self.val_flat != None:
                numberFlat = self.findFlat()
                if numberFlat == 0:
                    print('fF',numberFlat)
                    self.add_flat()
            else: self.val_id_flat = None        
            if self.val_serKpu != None:
                self.findKpu()
            else: self.val_id_kpu = None
            if self.checkBox.isChecked():
                if self.val_serKpu == None:
                    self.text = 'Введите серийный номер КПУ'
                    raise ValueError
                if self.val_flat == None:   
                    self.text = 'Введите номер квартиры'
                    raise ValueError
                if self.val_type == None:
                    self.text = 'Введите тип счетчика'
                    raise ValueError
                if self.val_coef == None:
                    self.text = 'Введите коэффициент'
                    raise ValueError 
            if numberFlat == 1:
                print('fF',numberFlat)
                self.resize(800,300)
                self.insert_pu()
                if not self.box_work: self.close()
                if self.val_klemma == None: self.close()
                self.widget.setEnabled(False)
                self.widget_stZn.show()
                self.label_error.hide()
            elif numberFlat == -1: 
                print('fF',numberFlat)
                self.insert_pu()
                self.close()
        except ValueError:         
            pal = self.label_error.palette()
            pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
            self.label_error.setPalette(pal)
            #self.resize(self.label_error.sizeHint())    
            self.label_error.setText(self.text)        
            self.label_error.show() 
        except psycopg2.Error as err:       
            print("Error: ", err)
    
    def add_flat(self):
        self.resize(700,300)
        self.widget.setEnabled(False)
        self.widget_addFlat.show()
        self.label_error.hide()
        self.label_2.setText(str(self.val_flat) + ' квартиры нету в базе данных, хотите добавить?')
        val_entr=self.comboBox_entr.currentText()
        if val_entr == '': val_entr='1'
        self.comboBox_entrAdd.setCurrentText(val_entr)
        self.comboBox_entrAdd.model().item(0).setEnabled(False)        
    
    def cansel(self):
        self.resize(500,300)
        self.widget.setEnabled(True)
        self.widget_addFlat.hide()
        self.label_error.hide()
     
    def insert_flat(self):
        self.val_id_entr = int(self.list_id_entrance[self.comboBox_entrAdd.currentIndex()])
        self.val_comment = self.lineEdit_noteAdd.text()
        if self.val_comment == '': self.val_comment = None
        self.val_flatfloor = self.lineEdit_floorAdd.text()
        self.val_flatfloor = None if self.val_flatfloor == '' else int(self.val_flatfloor)
        cur = self.conn.cursor()
        sql_query = """INSERT INTO public.flat(id_entr, num_flat, fio, flatfloor)                                                                                             
                    VALUES (%s, %s, %s, %s)"""
        cur.execute(sql_query, (self.val_id_entr, self.val_flat, self.val_comment, self.val_flatfloor)) 
        #self.conn.commit()
        cur.close()
        self.cansel()
     
    def insert_pu(self): #переделать поиск нового оборудования
        cur = self.conn.cursor()
        sql_query = """INSERT INTO cnt.counter(klemma, id_kpu, id_entr, id_flat, 
                        id_marka, coefficient, serial_number, working_capacity, 
                        date_install, id_house, type_counter, consumption_coeff)                                                                                             
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_klemma;"""
        cur.execute(sql_query, (self.val_klemma, self.val_id_kpu, self.val_id_entr, self.val_id_flat, 
                    self.val_id_marka, self.val_coef, self.val_serial, self.box_work,
                    self.val_date, self.val_id_house, self.val_type, self.val_coefons)) 
        #self.conn.commit()
        data = cur.fetchall()
        cur.close()
        self.id_klemma=data[0][0]
        self.label.setText('id_klemma = ' + str(self.id_klemma))
        print('insert pu')

    def findFlat(self):
        cur = self.conn.cursor()
        flat_query = """SELECT
                            flat.id_flat
                        FROM
                            public.flat
                        left join public.entrance
                            on flat.id_entr = entrance.id_entr"""
        flat_query  = flat_query + " WHERE entrance.id_house = " + str(self.val_id_house)
        flat_query  = flat_query + " AND flat.num_flat = " + str(self.val_flat)
        cur.execute(flat_query)   
        self.list_id_flat = cur.fetchall()
        if len(self.list_id_flat)>0: self.val_id_flat = self.list_id_flat[0][0]
        else: self.val_id_flat = None
        return len(self.list_id_flat)
        
    def findKpu(self):
        cur = self.conn.cursor()
        kpu_query = """SELECT
                            kpu.id_kpu
                        FROM
                            cnt.kpu
                        inner join public.flat
                            on flat.id_entr = kpu.id_entr"""
        kpu_query  = kpu_query + " WHERE kpu.ser_num = " + str(self.val_serKpu)
        if self.val_id_flat != None:
            kpu_query  = kpu_query + " AND flat.id_flat = " + str(self.val_id_flat)
        elif self.val_id_entr != None:
            kpu_query  = kpu_query + " AND kpu.id_entr = " + str(self.val_id_entr)  
        cur.execute(kpu_query)
        self.list_id_kpu = cur.fetchall()
        if len(self.list_id_kpu) == 0: 
            self.text = 'В БД отсутсвует КПУ с данным серийным номером'
            if self.val_flat != None or self.val_entr != '':
                self.text = 'На заданном адресе не установлен данный КПУ'
            raise ValueError
        self.val_id_kpu = self.list_id_kpu[0][0]
        
    def insert_start_value(self):
        self.date_val = self.dateTimeEdit_date.dateTime().toString("yyyy-MM-dd hh:mm:00")
        self.st_value = self.doubleSpinBox_val.value()
        self.impulse_value = self.spinBox_imp.value()
        cur = self.conn.cursor()
        sql_query = """INSERT INTO cnt.start_value(id_klemma, date_val, st_value, impulse_value)                                                                                             
                    VALUES (%s, %s, %s, %s)"""
        cur.execute(sql_query, (self.id_klemma, self.date_val, self.st_value, self.impulse_value)) 
        #self.conn.commit()
        cur.close()
        self.close()

    def filtr(self):
            self.filtr_city()
            if (self.ser_kpu !=''):
                self.lineEdit_serKpu.setText(self.ser_kpu)
            self.comboBox_city.currentIndexChanged.connect(self.filtr_street)
            if (self.city!=''): 
                self.comboBox_city.setCurrentText(self.city)
            self.comboBox_street.currentIndexChanged.connect(self.filtr_house)
            if (self.street!=''):
                self.comboBox_street.setCurrentText(self.street)
            self.comboBox_house.currentIndexChanged.connect(self.filtr_entrance)
            if (self.house!=''):
                self.comboBox_house.setCurrentText(self.house)
            if (self.entr!=''):
                self.comboBox_entr.setCurrentText(self.entr)  
            self.filtr_marka()
            self.comboBox_type.currentIndexChanged.connect(self.filtr_marka)
            
    def filtr_city(self):
        self.comboBox_city.clear()        
        self.comboBox_city.id = []
        self.list_id_city = [0]
        self.comboBox_city.addItem('')
        cur = self.conn.cursor()
        city_query = """SELECT DISTINCT
                            city.city_name,	
                            city.id_city 
                        FROM
                            public.entrance
                            left join public.house
                                on house.id_house = entrance.id_house
                            left join public.street
                                on street.id_street = house.id_street
                            left join public.city
                                on city.id_city = street.id_city
                            order by city.city_name"""
        cur.execute(city_query)        
        data = cur.fetchall()
        for index,row in enumerate(data):           
            self.list_id_city.append(data[index][1])
            self.comboBox_city.addItem(str(data[index][0]))
        cur.close()
        
    def filtr_street(self):  
        self.comboBox_street.clear()        
        self.comboBox_street.id = []
        self.list_id_street = [0]
        self.comboBox_street.addItem('')
        cur = self.conn.cursor() 
        street_query = """SELECT DISTINCT
                            street.street_name,	
                            street.id_street 
                        FROM
                            public.entrance
                            left join public.house
                                on house.id_house = entrance.id_house
                            left join public.street
                                on street.id_street = house.id_street"""                    
        street_query = street_query + " WHERE street.id_city = " + str(self.list_id_city[self.comboBox_city.currentIndex()]) + " order by street.street_name"                      
        cur.execute(street_query)        
        data = cur.fetchall()
        for index,row in enumerate(data):   
            self.list_id_street.append(data[index][1])
            self.comboBox_street.addItem(str(data[index][0]))    
        cur.close()
        
    def filtr_house(self):
        self.comboBox_house.clear()        
        self.comboBox_house.id = []
        self.list_id_house = [0]
        self.comboBox_house.addItem('')
        cur = self.conn.cursor()
        house_query = """SELECT DISTINCT
                            house.house_number,	
                            house.id_house 
                        FROM
                            public.entrance
                            left join public.house
                                on house.id_house = entrance.id_house"""
        house_query = house_query + " WHERE house.id_street = " + str(self.list_id_street[self.comboBox_street.currentIndex()]) + " order by house.house_number"       
        cur.execute(house_query)   
        data = cur.fetchall()
        for index,row in enumerate(data):  
            self.list_id_house.append(data[index][1])  
            self.comboBox_house.addItem(str(data[index][0]))          
        cur.close()
        
    def filtr_entrance(self):
        self.comboBox_entr.clear()        
        self.comboBox_entr.id = [] 
        self.comboBox_entrAdd.clear()        
        self.comboBox_entrAdd.id = [] 
        self.list_id_entrance = [0]
        self.comboBox_entr.addItem('')
        self.comboBox_entrAdd.addItem('')
        cur = self.conn.cursor()
        entrance_query = """SELECT
                            entrance.num_entr,	
                            entrance.id_entr                             
                        FROM
                            public.entrance"""                            
        entrance_query = entrance_query + " WHERE entrance.id_house = " + str(self.list_id_house[self.comboBox_house.currentIndex()]) + " order by cast(entrance.num_entr as integer)"
        cur.execute(entrance_query) 
        data = cur.fetchall()
        for index,row in enumerate(data):
            self.list_id_entrance.append(data[index][1])        
            self.comboBox_entr.addItem(str(data[index][0]))
            self.comboBox_entrAdd.addItem(str(data[index][0]))
        cur.close()
        
    def filtr_marka(self):
        self.comboBox_marka.clear()        
        self.comboBox_marka.id = [] 
        self.list_id_marka = [0]
        self.comboBox_marka.addItem('')
        cur = self.conn.cursor()
        entrance_query = """SELECT
                            marka.name_marka,
                            marka.id_marka                            
                        FROM
                            cnt.marka"""                            
        entrance_query = entrance_query + " WHERE marka.type_counter = " + str(self.comboBox_type.currentIndex())
        entrance_query = entrance_query + " order by marka.name_marka"
        cur.execute(entrance_query) 
        data = cur.fetchall()
        for index,row in enumerate(data):
            self.list_id_marka.append(data[index][1])        
            self.comboBox_marka.addItem(str(data[index][0]))        
        cur.close()
        
class Info_Pu(QtWidgets.QWidget, info_PU_ui.Ui_Form):
    def __init__(self, id_pu, conn):
        super().__init__()
        self.setupUi(self)
        self.conn = conn
        self.id_pu = id_pu
        self.widget_puNew.hide()
        self.label_error.hide()
        self.resize(550,350)
        self.setWindowTitle('Изменить информацию о ПУ')
        #self.pushButton_kpu.clicked.connect(self.open_kpu)
        #self.pushButton_save.clicked.connect(self.verify)
        #self.pushButton_replace.clicked.connect(self.replace)
        #self.pushButton_replaceNew.clicked.connect(self.verify)
        #self.pushButton_canselNew.clicked.connect(self.verify)
        #self.pushButton_addStart.clicked.connect(self.add_start)
        #self.pushButton_showVal.clicked.connect(self.verify)
        self.lineEdit_serKpu.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.lineEdit_flat.setValidator(QRegExpValidator(QRegExp("[1-9][0-9]{,3}")))
        self.lineEdit_klemma.setValidator(QRegExpValidator(QRegExp("[1-9][0-9]")))
        self.lineEdit_coefons.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.lineEdit_coef.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.dateEdit_dateInstall.setDate(datetime.date.today())
        self.dateTimeEdit_dateNew.setDateTime(datetime.datetime.today().replace(minute=0, second=0))
        print('0')
        self.select()
        print('1')
        self.filtr()
        self.filling()
        self.show()
    
    def filling(self):
        pass
        self.comboBox_city.setCurrentText(self.city_name)
        self.comboBox_street.setCurrentText(self.street_name)
        self.comboBox_house.setCurrentText(self.house_number)
        self.comboBox_entr.setCurrentText(str(self.num_entr))
        self.lineEdit_floor.setText('' if self.flatfloor==None else str(self.flatfloor))
        self.lineEdit_serKpu.setText('' if self.ser_num_kpu==None else str(self.ser_num_kpu))
        self.lineEdit_serial.setText('' if self.ser_num_pu==None else str(self.ser_num_pu))
        self.lineEdit_flat.setText('' if self.flat==None else str(self.flat))
        self.comboBox_type.setCurrentText(self.type_pu)
        self.label_typeKPU.setText('' if self.type_kpu==None else str(self.type_kpu))
        self.label_dateLast.setText('' if self.last_date==None else str(self.last_date))
        self.label_value.setText('' if self.last_pok==None else str(self.last_pok))
        self.checkBox.setChecked(self.workability)
        self.lineEdit_klemma.setText('' if self.klemma==None else str(self.klemma))
        self.lineEdit_coef.setText('' if self.coefficient==None else str(self.coefficient))
        self.lineEdit_coefons.setText('' if self.consumption_coeff==None else str(self.consumption_coeff))
        self.comboBox_marka.setCurrentText(self.marka)
        if self.date_install == None: 
            self.dateEdit_install.hide()
            self.label_install.hide()
        else: self.dateEdit_install.setDate(self.date_install)
        if self.date_deinstall == None: 
            self.dateEdit_deinstall.hide()
            self.label_deinstall.hide()
        else: self.dateEdit_deinstall.setDate(self.date_deinstall)
        self.label.setText('id_klemma = ' + self.id_pu)
        
    def select(self):
        cur = self.conn.cursor()
        self.sql_query_flat = """SELECT  			 			
                          counter.id_flat
                        FROM
                          cnt.counter
                        WHERE counter.id_klemma = %s"""
        cur.execute(self.sql_query_flat, (self.id_pu, ))
        flat = cur.fetchall()
        self.sql_query = """SELECT  			 			
                          counter.consumption_coeff, city.city_name,
                          street.street_name, house.house_number,
                          entrance.num_entr, flat.flatfloor, flat.num_flat,
                          case counter.type_counter 		
                            when 1 then 'ГВС'
                            when 2 then 'ХВС'
                            when 3 then 'Т'
                            when 4 then 'Э' 
                          end AS Тип, counter.serial_number,		
                          kpu.ser_num, kpu.type_kpu, counter.klemma,			
                          marka.name_marka, counter.coefficient, 
                          counter.last_pok, counter.date_install,
                          counter.date_deinstall, counter.working_capacity,
                          counter.last_date
                        FROM
                          cnt.counter"""
        if flat[0][0] == None:
            print('none')
            self.sql_query = self.sql_query + """
                          left join public.entrance
                            on entrance.id_entr = counter.id_entr"""
        else:
            print('yes')
            self.sql_query = self.sql_query + """
                          left join public.flat
                            on flat.id_flat = counter.id_flat
                          left join public.entrance
                            on entrance.id_entr = flat.id_entr  """
        self.sql_query = self.sql_query + """                    
                          inner join cnt.kpu
                            on counter.id_kpu=kpu.id_kpu
                          inner join cnt.marka
                            on counter.id_marka = marka.id_marka
                          inner join public.house
                            on house.id_house = entrance.id_house
                          inner join public.street
                            on street.id_street = house.id_street
                          inner join public.city
                            on city.id_city = street.id_city
                        WHERE counter.id_klemma = %s"""
        print(self.sql_query)
        cur.execute(self.sql_query, (self.id_pu, ))
        data = cur.fetchall()
        print('000')
        cur.close()
        self.consumption_coeff = data[0][0]
        self.city_name = data[0][1]
        self.street_name = data[0][2]
        self.house_number = data[0][3]
        self.num_entr = data[0][4]
        self.flatfloor = data[0][5]
        self.flat = data[0][6]
        self.type_pu = data[0][7]
        self.ser_num_pu = data[0][8]
        self.ser_num_kpu = data[0][9]
        self.type_kpu = data[0][10]
        self.klemma = data[0][11]
        self.marka = data[0][12]
        self.coefficient = data[0][13]
        self.last_pok = data[0][14]
        self.date_install = data[0][15]
        self.date_deinstall = data[0][16]
        self.workability = data[0][17]
        self.last_date = data[0][18]
 
    def open_kpu(self):
        self.kpu = kpu.Kpu(self.conn, self.id_entr)
        self.close()
        
    def save(self):
        self.close()

    def verify(self): #Доработать ошибки
        try:
            text='Введено некорректное значение'   
            if self.comboBox_house.currentText()=='' and self.comboBox_serKpu.currentText()=='': 
                text='Введите номер дома или серийный номер КПУ'
                raise ValueError
            if self.comboBox_flat.currentText()=='' and self.comboBox_serKpu.currentText()=='': 
                text='Введите номер квартиры или серийный номер КПУ'
                raise ValueError    
            self.val_serKpu = str(self.lineEdit_serKpu.text())
            self.val_serKpu = None if self.val_serKpu == '' else int(self.val_serKpu)
            
            self.val_adress = int(self.spinBox_adress.value())
            #self.val_id_entr = int(self.list_id_entrance[self.comboBox_entrance.currentIndex()])
            self.val_type = int(self.comboBox_type.currentText())
            self.val_serial = str(self.lineEdit_serial.text())
            self.val_serial = None if self.val_serial == '' else int(self.val_serial)
            self.val_floor = str(self.lineEdit_floor.text())
            self.val_floor = None if self.val_floor == '' else int(self.val_floor)
            self.val_note = self.textEdit_note.toPlainText()
            if self.val_note == '': self.val_note = None
            self.val_work = int(self.checkBox.isChecked())
            if self.id_kpu=='-1' and not self.flagInsert:
                self.insert()
            if self.id_kpu!='-1' or self.flagInsert:
                self.update()
        except ValueError:         
                pal = self.label_error.palette()
                pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
                self.label_error.setPalette(pal)
                #self.resize(self.label_error.sizeHint())    
                self.label_error.setText(text)        
                self.label_error.show()  

    def insert(self):
        cur = self.conn.cursor()
        sql_query = """INSERT INTO cnt.kpu(adress, id_entr, type_kpu, ser_num, 
                                            floor, note, workability)                                                                                             
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cur.execute(sql_query, (self.val_adress, self.val_id_entr, self.val_type, self.val_serial, self.val_floor, self.val_note, self.val_work))                
        #self.conn.commit()
        cur.close() 
        self.flagInsert = True
        self.tabWidget.setTabEnabled(1,True)
        self.tabWidget.setCurrentIndex(1)
        self.close()

    def update(self):
        cur = self.conn.cursor()
        sql_query = """ UPDATE cnt.kpu
                        SET adress=%s, id_entr=%s, type_kpu=%s, ser_num=%s, floor=%s, note=%s, workability=%s 
                        WHERE id_kpu=%s"""
        cur.execute(sql_query, (self.val_adress, self.val_id_entr, self.val_type, self.val_serial, self.val_floor, self.val_note, self.val_work, self.id_kpu))               
        #self.conn.commit()
        cur.close()
        if self.flagInsert:
            self.tabWidget.setCurrentIndex(1)
        self.close()

    def add_start(self):
        self.close()
        
    def replace(self):
        pass
        
    def filtr(self):
            self.filtr_city()
            self.comboBox_city.currentIndexChanged.connect(self.filtr_street)
            self.comboBox_street.currentIndexChanged.connect(self.filtr_house)
            self.comboBox_house.currentIndexChanged.connect(self.filtr_entrance) 
            self.filtr_marka()
            self.comboBox_type.currentIndexChanged.connect(self.filtr_marka)
            
    def filtr_city(self):
        self.comboBox_city.clear()        
        self.comboBox_city.id = []
        self.list_id_city = [0]
        self.comboBox_city.addItem('')
        cur = self.conn.cursor()
        city_query = """SELECT DISTINCT
                            city.city_name,	
                            city.id_city 
                        FROM
                            public.entrance
                            left join public.house
                                on house.id_house = entrance.id_house
                            left join public.street
                                on street.id_street = house.id_street
                            left join public.city
                                on city.id_city = street.id_city
                            order by city.city_name"""
        cur.execute(city_query)        
        data = cur.fetchall()
        for index,row in enumerate(data):           
            self.list_id_city.append(data[index][1])
            self.comboBox_city.addItem(str(data[index][0]))
        cur.close()
        
    def filtr_street(self):  
        self.comboBox_street.clear()        
        self.comboBox_street.id = []
        self.list_id_street = [0]
        self.comboBox_street.addItem('')
        cur = self.conn.cursor() 
        street_query = """SELECT DISTINCT
                            street.street_name,	
                            street.id_street 
                        FROM
                            public.entrance
                            left join public.house
                                on house.id_house = entrance.id_house
                            left join public.street
                                on street.id_street = house.id_street"""                    
        street_query = street_query + " WHERE street.id_city = " + str(self.list_id_city[self.comboBox_city.currentIndex()]) + " order by street.street_name"                      
        cur.execute(street_query)        
        data = cur.fetchall()
        cur.close()
        for index,row in enumerate(data):   
            self.list_id_street.append(data[index][1])
            self.comboBox_street.addItem(str(data[index][0]))    
        
    def filtr_house(self):
        self.comboBox_house.clear()        
        self.comboBox_house.id = []
        self.list_id_house = [0]
        self.comboBox_house.addItem('')
        cur = self.conn.cursor()
        house_query = """SELECT DISTINCT
                            house.house_number,	
                            house.id_house 
                        FROM
                            public.entrance
                            left join public.house
                                on house.id_house = entrance.id_house"""
        house_query = house_query + " WHERE house.id_street = " + str(self.list_id_street[self.comboBox_street.currentIndex()]) + " order by house.house_number"       
        cur.execute(house_query)   
        data = cur.fetchall()
        for index,row in enumerate(data):  
            self.list_id_house.append(data[index][1])  
            self.comboBox_house.addItem(str(data[index][0]))          
        cur.close()
        
    def filtr_entrance(self):
        self.comboBox_entr.clear()        
        self.comboBox_entr.id = [] 
        self.list_id_entrance = [0]
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
        for index,row in enumerate(data):
            self.list_id_entrance.append(data[index][1])        
            self.comboBox_entr.addItem(str(data[index][0]))
        cur.close()
        
    def filtr_marka(self):
        self.comboBox_marka.clear()        
        self.comboBox_marka.id = [] 
        self.comboBox_markaNew.clear()        
        self.comboBox_markaNew.id = [] 
        self.list_id_marka = [0]
        self.comboBox_marka.addItem('')
        self.comboBox_markaNew.addItem('')
        cur = self.conn.cursor()
        entrance_query = """SELECT
                            marka.name_marka,
                            marka.id_marka                            
                        FROM
                            cnt.marka"""                            
        entrance_query = entrance_query + " WHERE marka.type_counter = " + str(self.comboBox_type.currentIndex())
        entrance_query = entrance_query + " order by marka.name_marka"
        cur.execute(entrance_query) 
        data = cur.fetchall()
        for index,row in enumerate(data):
            self.list_id_marka.append(data[index][1])        
            self.comboBox_marka.addItem(str(data[index][0])) 
            self.comboBox_markaNew.addItem(str(data[index][0]))
        cur.close()
            
        