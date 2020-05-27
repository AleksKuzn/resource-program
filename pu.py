import sys
import psycopg2
import fdb
import datetime
import traceback
import PU_ui, add_PU_ui, info_PU_ui, KPU_ui, scaut    
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from datetime import timedelta 
       
class Pu(QtWidgets.QWidget, PU_ui.Ui_Form):
    def __init__(self, conn, id_kpu):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Приборы Учета')
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
        self.sql_query = self.sql_query + self.sql_query_where + " ORDER BY city.city_name DESC, street.street_name DESC, cast(substring(house.house_number from \'^[0-9]+\') as integer) DESC, cast(entrance.num_entr as integer) DESC, flat.num_flat DESC, counter.type_counter DESC"       
        self.sql_query2 = """SELECT
                                counter.id_klemma, city.city_name,
                                street.street_name, house.house_number,
                                entrance.num_entr, null, null,
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
                                left join cnt.kpu
                                on counter.id_kpu=kpu.id_kpu
                                left join public.entrance
                                on entrance.id_entr = kpu.id_entr
                                left join cnt.marka
                                on counter.id_marka = marka.id_marka
                                left join public.house
                                on house.id_house = entrance.id_house
                                left join public.street
                                on street.id_street = house.id_street
                                left join public.city
                                on city.id_city = street.id_city
                            WHERE counter.id_flat is null"""
        self.sql_query2 = self.sql_query2 + self.sql_query_where + " ORDER BY city.city_name DESC, street.street_name DESC, cast(substring(house.house_number from \'^[0-9]+\') as integer) DESC, cast(entrance.num_entr as integer) DESC, counter.type_counter DESC"     
        cur = self.conn.cursor()
        cur.execute(self.sql_query)
        data1 = cur.fetchall()
        cur.execute(self.sql_query2)
        data2 = cur.fetchall()
        data = data2+data1
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
        self.checkType()
        self.checkRS485()
        self.checkBox_type.stateChanged.connect(self.checkType)
        self.checkBox_rs485.stateChanged.connect(self.checkRS485)
        self.resize(500,300)
        self.lineEdit_serKpu.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.lineEdit_flat.setValidator(QRegExpValidator(QRegExp("[1-9][0-9]{,3}")))
        self.lineEdit_klemma.setValidator(QRegExpValidator(QRegExp("[1-9][0-9]")))
        self.pushButton_addStart.clicked.connect(self.insert_start_value)
        self.lineEdit_coefons.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.lineEdit_coef.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.lineEdit_floorAdd.setValidator(QRegExpValidator(QRegExp("[0-9][0-9]")))
        self.dateEdit_dateInstall.setDate(datetime.date.today())
        self.dateTimeEdit_date.setDateTime(datetime.datetime.today().replace(minute=0, second=0))
        self.filtr()
        self.pushButton_save.clicked.connect(self.verify)
        self.pushButton_cansel.clicked.connect(self.cansel)
        self.pushButton_addFlat.clicked.connect(self.insert_flat)
        self.setWindowTitle('Добавить квартирный ПУ')
        self.show()
    
    def add_flat(self):
        self.resize(700,300)
        self.widget.setEnabled(False)
        self.widget_addFlat.show()
        self.label_error.hide()
        self.label_2.setText(str(self.val_flat) + ' квартиры нету в базе данных, хотите добавить?')
        if self.val_entr == '': val_entr = '1'
        else: val_entr = self.val_entr
        self.comboBox_entrAdd.setCurrentText(val_entr)
        self.comboBox_entrAdd.model().item(0).setEnabled(False)        
    
    def cansel(self):
        self.resize(500,300)
        self.widget.setEnabled(True)
        self.widget_addFlat.hide()
        self.label_error.hide()
     
    def checkType(self):
        if self.checkBox_type.isChecked():
            #self.label_entr.setEnabled(True)
            #self.comboBox_entr.setEnabled(True)
            #self.label_coefons.setEnabled(True)
            self.lineEdit_coefons.setEnabled(True)
        else:
            #self.label_entr.setEnabled(False)
            #self.comboBox_entr.setEnabled(False)
            #self.label_coefons.setEnabled(False)
            self.lineEdit_coefons.setEnabled(False)
            self.lineEdit_coefons.setText('1')
    
    def checkRS485(self):
        if self.checkBox_rs485.isChecked():
            #self.label_serKpu.setEnabled(False)
            self.lineEdit_serKpu.setEnabled(False)
           # self.label_klemma.setEnabled(False)
            self.lineEdit_klemma.setEnabled(False)
            self.lineEdit_coef.setEnabled(False)
            self.lineEdit_serKpu.setText('')
            self.lineEdit_klemma.setText('')
            self.lineEdit_coef.setText('')
        else:
            #self.label_serKpu.setEnabled(True)
            self.lineEdit_serKpu.setEnabled(True)
            #self.label_klemma.setEnabled(True)
            self.lineEdit_klemma.setEnabled(True)
            self.lineEdit_coef.setEnabled(True)
    
    def create_connection_firebird(self):
        try:
            connection = None
            connection = fdb.connect(
                host=self.ip_rassbery,
                database=self.fdb_path,
                user=self.fdb_login,
                password=self.fdb_password
            )
            print("\nConnection to the FireBird DB successful.\nhost = ",self.ip_rassbery,"\nname = ",self.fdb_path,"\nuser = ",self.fdb_login,"\npassword = ",self.fdb_password)
            self.insert_fdb(connection)
            connection.close()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Не удалось подключиться к локальной базе данных.")
            msg.setInformativeText("Хотите отредактировать данные СКАУТ или продолжить без добавления КПУ в базу данных FireBird?")
            msg.setDetailedText("host = "+str(self.ip_rassbery)+"\nname = "+str(self.fdb_path)+"\nuser = "+str(self.fdb_login)+"\npassword = "+str(self.fdb_password))
            scautButton = msg.addButton('СКАУТ', QMessageBox.AcceptRole)
            continueButton = msg.addButton('Продолжить', QMessageBox.RejectRole)
            msg.exec()
            if msg.clickedButton() == scautButton:
                self.add_scaut = scaut.Add_Scaut(self.val_id_entr,self.conn)
            if msg.clickedButton() == continueButton:
                self.checkBox.setChecked(False)
                self.box_work = False
            print (traceback.format_exc())
    
    def findFlat(self):
        cur = self.conn.cursor()
        flat_query = """SELECT
                            flat.id_flat, flat.id_entr
                        FROM
                            public.flat
                        left join public.entrance
                            on flat.id_entr = entrance.id_entr"""
        flat_query  = flat_query + " WHERE entrance.id_house = " + str(self.val_id_house) + " AND flat.num_flat = " + str(self.val_flat)
        cur.execute(flat_query)
        self.list_id_flat = cur.fetchall()
        if len(self.list_id_flat)==0:
            self.val_id_flat = None
            self.add_flat()
            self.flag_work = False
        else: self.val_id_flat = self.list_id_flat[0][0]
        if self.val_id_entr == None: self.val_id_entr = self.list_id_flat[0][1]
        
    def findKpu(self):
        cur = self.conn.cursor()
        kpu_query = """SELECT
                            kpu.id_kpu, kpu.id_entr, kpu.adress, kpu.type_kpu, kpu.workability
                        FROM
                            cnt.kpu
                        left join public.flat
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
            self.flag_work = False
        elif self.list_id_kpu[0][4] == 0:
            self.text = 'Состояние выбранного КПУ - неработоспособен'
            self.flag_work = False
        else: 
            self.val_id_kpu = self.list_id_kpu[0][0]
            if self.val_id_entr == None: self.val_id_entr = self.list_id_kpu[0][1]
            self.val_adress = self.list_id_kpu[0][2]
            self.val_type_kpu = self.list_id_kpu[0][3]

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

    def insert_flat(self):
        self.val_id_entr = int(self.list_id_entrance[self.comboBox_entrAdd.currentIndex()])
        self.val_comment = self.lineEdit_noteAdd.text()
        if self.val_comment == '': self.val_comment = None
        self.val_flatfloor = self.lineEdit_floorAdd.text()
        self.val_flatfloor = None if self.val_flatfloor == '' else int(self.val_flatfloor)
        cur = self.conn.cursor()
        sql_query = """INSERT INTO public.flat(id_entr, num_flat, fio, flatfloor)                                                                                             
                    VALUES (%s, %s, %s, %s) RETURNING id_flat;"""
        cur.execute(sql_query, (self.val_id_entr, self.val_flat, self.val_comment, self.val_flatfloor)) 
        self.conn.commit()
        data = cur.fetchall()
        self.val_id_flat=data[0][0]
        cur.close()
        self.cansel()

    def insert_pu(self):
        if self.val_house_counter == False: 
            self.val_id_entr = None
            self.val_id_house = None
        sql_query = """INSERT INTO cnt.counter(klemma, id_kpu, id_entr, id_flat, 
                        id_marka, coefficient, serial_number, working_capacity, 
                        date_install, id_house, type_counter, consumption_coeff, type_connection)                                                                                             
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_klemma;"""           
        cur = self.conn.cursor()
        cur.execute(sql_query, (self.val_klemma, self.val_id_kpu, self.val_id_entr, self.val_id_flat, 
                    self.val_id_marka, self.val_coef, self.val_serial, self.box_work,
                    self.val_date, self.val_id_house, self.val_type, self.val_coefons, self.val_rs485)) 
        self.conn.commit()
        data = cur.fetchall()
        cur.close()
        self.id_klemma=data[0][0]

    def insert_fdb(self,fireBird):
        try:
            if self.box_rs485 == False:
                sql_query = """ SELECT ID_KPU FROM KPU 
                                WHERE TYPE_KPU = ? AND ADRESS = ? """
                cur = fireBird.cursor()
                cur.execute(sql_query, (self.val_type_kpu, self.val_adress))
                data = cur.fetchall()
                self.id_kpu_fdb = data[0][0]
                sql_query = """ INSERT INTO COUNTER(KLEMMA, ID_KPU, TYPE_COUNTER)
                                VALUES (?, ?, ?) """
                cur.execute(sql_query, (self.val_klemma, self.id_kpu_fdb, self.val_type))
                self.conn.commit()
                cur.close()
            if self.box_rs485 == True:
                sql_query = """ INSERT INTO COUNTER(TYPE_COUNTER, SER_NUM)
                                VALUES (?, ?) """
                cur = fireBird.cursor()
                cur.execute(sql_query, (self.val_type, self.val_serial))
                self.conn.commit()
                cur.close()
        except:
            print (traceback.format_exc())

    def insert_start_value(self):
        self.date_val = self.dateTimeEdit_date.dateTime().toString("yyyy-MM-dd hh:mm:00")
        self.st_value = self.doubleSpinBox_val.value()
        self.impulse_value = self.spinBox_imp.value()
        cur = self.conn.cursor()
        sql_query = """INSERT INTO cnt.start_value(id_klemma, date_val, st_value, impulse_value)                                                                                             
                    VALUES (%s, %s, %s, %s)"""
        cur.execute(sql_query, (self.id_klemma, self.date_val, self.st_value, self.impulse_value)) 
        self.conn.commit()
        cur.close()
        QMessageBox.information(self, 'Информация', 'Стартовые значения успешно добавлены')
        self.close()
        self.info_pu = Info_Pu(self.id_klemma, self.conn)

    def paint_text(self,name_label,text,color_text):
        pal = name_label.palette()
        pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor(color_text))
        name_label.setPalette(pal)
        #self.resize(self.label_error.sizeHint())
        name_label.setText(text)
        name_label.show()

    def select_parameters_firebird(self):
        sql_query = """SELECT ip_rassbery, fdb_login, fdb_password, fdb_path
                       FROM save.login_data
                       WHERE id_entr = %s"""
        cur = self.conn.cursor()
        cur.execute(sql_query, (self.val_id_entr, ))
        data = cur.fetchall()
        cur.close()
        self.ip_rassbery = data[0][0]
        self.fdb_login = data[0][1]
        self.fdb_password = data[0][2]
        self.fdb_path = data[0][3]

    def verify(self):
        try:
            self.label_error.hide()
            self.lineEdit_serial.setStyleSheet('background : #FFFFFF;')
            self.lineEdit_serKpu.setStyleSheet('background : #FFFFFF;')
            self.lineEdit_klemma.setStyleSheet('background : #FFFFFF;')
            self.comboBox_city.setStyleSheet('background : #FFFFFF;')
            self.lineEdit_coef.setStyleSheet('background : #FFFFFF;')
            self.comboBox_street.setStyleSheet('background : #FFFFFF;')
            self.comboBox_house.setStyleSheet('background : #FFFFFF;')
            self.comboBox_entr.setStyleSheet('background : #FFFFFF;')
            self.flag_work = True
            self.text='Введено некорректное значение'
            self.val_serKpu = None if self.lineEdit_serKpu.text() == '' else int(self.lineEdit_serKpu.text())
            if self.comboBox_house.currentText() != '': self.val_id_house = int(self.list_id_house[self.comboBox_house.currentIndex()])
            else: self.val_id_house = None     
            self.val_street = self.comboBox_street.currentText()
            self.val_city = self.comboBox_city.currentText()
            self.val_entr = str(self.comboBox_entr.currentText())
            if self.val_entr != '': self.val_id_entr = int(self.list_id_entrance[self.comboBox_entr.currentIndex()])
            else: self.val_id_entr = None
            self.val_flat = None if self.lineEdit_flat.text() == '' else int(self.lineEdit_flat.text())
            self.val_type = int(self.comboBox_type.currentIndex())
            if self.val_type == 0: self.val_type = None
            self.val_klemma = None if self.lineEdit_klemma.text() == '' else int(self.lineEdit_klemma.text())
            self.val_serial = None if self.lineEdit_serial.text() == '' else str(self.lineEdit_serial.text()) 
            self.val_coef = None if self.lineEdit_coef.text() == '' else int(self.lineEdit_coef.text())
            self.val_coefons = 1 if self.lineEdit_coefons.text() == '' else int(self.lineEdit_coefons.text())
            self.val_id_marka = int(self.list_id_marka[self.comboBox_marka.currentIndex()])
            if self.val_id_marka == 0: self.val_id_marka = None
            self.val_date = self.dateEdit_dateInstall.date().toString("yyyy-MM-dd")
            self.val_house_counter = self.checkBox_type.isChecked()
            self.box_work = self.checkBox.isChecked()
            self.val_rs485 = 2 if self.checkBox_rs485.isChecked() else 1 
            if self.box_work:
                if self.val_rs485 == 1:
                    if self.val_serKpu == None: 
                        self.lineEdit_serKpu.setStyleSheet('background : #FDDDE6;')
                        self.flag_work = False
                    if self.val_klemma == None:
                        self.lineEdit_klemma.setStyleSheet('background : #FDDDE6;')
                        self.flag_work = False
                    if self.val_coef == None:
                        self.lineEdit_coef.setStyleSheet('background : #FDDDE6;')
                        self.flag_work = False
                if self.val_rs485 == 2:    
                    if self.val_serial == None:
                        self.lineEdit_serial.setStyleSheet('background : #FDDDE6;')
                        self.flag_work = False
                    if self.val_id_entr == None and self.val_flat == None:
                        self.paint_text(self.label_error,'Введите номер подъезда или номер квартиры',"red")
                        self.flag_work = False
            if self.val_flat != None: 
                if self.val_city == '':
                    self.comboBox_city.setStyleSheet('background : #FDDDE6;')
                    self.flag_work = False
                if self.val_street == '':
                    self.comboBox_street.setStyleSheet('background : #FDDDE6;')
                    self.flag_work = False
                if self.val_house == '':
                    self.comboBox_house.setStyleSheet('background : #FDDDE6;')
                    self.flag_work = False
                else: self.findFlat()
            else: self.val_id_flat = None   
            if self.val_serKpu != None: 
                self.findKpu()
            else: self.val_id_kpu = None    
            if self.flag_work:
                self.select_parameters_firebird()
                self.create_connection_firebird()
                self.insert_pu()
                self.label.setText('id_klemma = ' + str(self.id_klemma))
                QMessageBox.information(self, 'Информация', 'ПУ успешно добавлен')
                if self.val_rs485 == 1:
                    self.resize(800,300)
                    self.widget.setEnabled(False)
                    self.widget_stZn.show()
                    self.label_error.hide()
                else: 
                    self.close()
                    self.info_pu = Info_Pu(self.id_klemma, self.conn)
        except:
            print (traceback.format_exc())
            self.paint_text(self.label_error,self.text,"red")

class Info_Pu(QtWidgets.QWidget, info_PU_ui.Ui_Form):
    def __init__(self, id_pu, conn):
        try:
            super().__init__()
            self.setupUi(self)
            self.conn = conn
            self.id_counter = id_pu
            self.widget_puNew.hide()
            self.widget_addFlat.hide()
            self.label_error.hide()
            self.resize(550,350)
            self.setWindowTitle('Информация о ПУ')
            self.checkType()
            self.checkRS485()
            self.checkBox_type.stateChanged.connect(self.checkType)
            self.checkBox_rs485.stateChanged.connect(self.checkRS485)
            self.checkBox_startZn.stateChanged.connect(self.checkAddStZn)
            self.checkBox_rs485New.stateChanged.connect(self.checkRS485_new)
            self.pushButton_save.clicked.connect(self.verify)
            self.pushButton_replace.clicked.connect(self.open_replace)
            self.pushButton_replaceNew.clicked.connect(self.replace_counter)
            self.pushButton_canselNew.clicked.connect(self.canselNew)
            self.pushButton_cansel.clicked.connect(self.cansel)
            self.pushButton_addFlat.clicked.connect(self.insert_flat)
            self.pushButton_addStart.clicked.connect(self.save_start_value)
            self.pushButton_showVal.clicked.connect(self.show_value)
            self.lineEdit_serKpu.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
            self.lineEdit_flat.setValidator(QRegExpValidator(QRegExp("[1-9][0-9]{,3}")))
            self.lineEdit_klemma.setValidator(QRegExpValidator(QRegExp("[1-9][0-9]")))
            self.lineEdit_coefons.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
            self.lineEdit_coef.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
            self.lineEdit_klemmaNew.setValidator(QRegExpValidator(QRegExp("[1-9][0-9]")))
            self.lineEdit_coefonsNew.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
            self.lineEdit_coefNew.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
            self.lineEdit_floorAdd.setValidator(QRegExpValidator(QRegExp("[0-9][0-9]")))
            self.pushButton_install.clicked.connect(self.select_date_install)
            self.pushButton_deinstall.clicked.connect(self.select_date_deinstall)
            self.pushButton_select_impulse.clicked.connect(self.select_impulse) 
            self.id_pu = id_pu
            self.select()
            self.filtr()
            self.filling()
            self.select_start_value()
            self.select_history()
            self.show_value()
            self.show()
        except :
            print (traceback.format_exc())
    
    def add_flat(self):
        self.resize(800,350)
        self.pushButton_save.setEnabled(False)
        self.pushButton_replace.setEnabled(False)
        self.pushButton_addStart.setEnabled(False)
        self.widget_addFlat.show()
        self.label_error.hide()
        self.label_2.setText(str(self.val_flat) + ' квартиры нету в базе данных, хотите добавить?')
        if self.val_entr == '': val_entr = '1'
        else: val_entr = self.val_entr
        self.comboBox_entrAdd.setCurrentText(val_entr)
        self.comboBox_entrAdd.model().item(0).setEnabled(False) 
    
    def cansel(self):
        self.resize(550,350)
        self.pushButton_save.setEnabled(True)
        self.pushButton_replace.setEnabled(True)
        self.pushButton_addStart.setEnabled(True)
        self.widget_addFlat.hide()
        self.label_error.hide()
    
    def canselNew(self):
        self.resize(550,350)
        self.widget_puNew.hide()
        self.label_error.hide()
        self.pushButton_save.setEnabled(True)
        self.pushButton_replace.setEnabled(True)
        self.pushButton_addStart.setEnabled(True)
        self.checkBox.setChecked(self.workability)
    
    def checkType(self):
        if self.checkBox_type.isChecked():
            self.lineEdit_coefons.setEnabled(True)
        else:
            self.lineEdit_coefons.setEnabled(False)
            self.lineEdit_coefons.setText('1')
    
    def checkRS485(self):
        if self.checkBox_rs485.isChecked():
            self.lineEdit_serKpu.setEnabled(False)
            self.lineEdit_klemma.setEnabled(False)
            self.lineEdit_coef.setEnabled(False)
            self.lineEdit_serKpu.setText('')
            self.lineEdit_klemma.setText('')
            self.lineEdit_coef.setText('')
        else:
            self.lineEdit_serKpu.setEnabled(True)
            self.lineEdit_klemma.setEnabled(True)
            self.lineEdit_coef.setEnabled(True)
            
    def checkAddStZn(self):
        if self.checkBox_startZn.isChecked():
            self.widget_startZn.show()
        else:
            self.widget_startZn.hide()
    
    def checkRS485_new(self):
        if self.checkBox_rs485New.isChecked():
            self.lineEdit_serKpuNew.setEnabled(False)
            self.lineEdit_klemmaNew.setEnabled(False)
            self.lineEdit_coefNew.setEnabled(False)
            self.lineEdit_klemmaNew.setText('')
            self.lineEdit_coefNew.setText('')
            self.checkBox_startZn.setChecked(False)
            self.checkBox_startZn.setEnabled(False)
        else:
            self.lineEdit_serKpuNew.setEnabled(True)
            self.lineEdit_klemmaNew.setEnabled(True)
            self.lineEdit_coefNew.setEnabled(True)
            self.checkBox_startZn.setChecked(True)
            self.checkBox_startZn.setEnabled(True)
            
    def create_connection_firebird(self):
        try:
            self.connection = None
            self.connection = fdb.connect(
                host=self.ip_rassbery,
                database=self.fdb_path,
                user=self.fdb_login,
                password=self.fdb_password
            )
            print("\nConnection to the FireBird DB successful.\nhost = ",self.ip_rassbery,"\nname = ",self.fdb_path,"\nuser = ",self.fdb_login,"\npassword = ",self.fdb_password)
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Не удалось подключиться к локальной базе данных.")
            msg.setInformativeText("Хотите отредактировать данные СКАУТ или продолжить без добавления КПУ в базу данных FireBird?")
            msg.setDetailedText("host = "+str(self.ip_rassbery)+"\nname = "+str(self.fdb_path)+"\nuser = "+str(self.fdb_login)+"\npassword = "+str(self.fdb_password))
            scautButton = msg.addButton('СКАУТ', QMessageBox.AcceptRole)
            continueButton = msg.addButton('Продолжить', QMessageBox.RejectRole)
            msg.exec()
            if msg.clickedButton() == scautButton:
                self.add_scaut = scaut.Add_Scaut(self.val_id_entr,self.conn)
            if msg.clickedButton() == continueButton:
                self.checkBox.setChecked(False)
                self.val_workability = False
            print (traceback.format_exc())
    
    def deleted_fdb(self,fireBird):
        try:
            sql_query = """ DELETE FROM COUNTER
                            WHERE ID_KLEMMA=?"""
            cur = fireBird.cursor()            
            cur.execute(sql_query, (self.id_klemma_fdb, )) 
            self.conn.commit()
            cur.close()
        except:
            print (traceback.format_exc())
     
    def filling(self):
        if self.workability: self.pushButton_replace.show()
        else: self.pushButton_replace.hide()
        self.comboBox_city.setCurrentText(self.city_name)
        self.comboBox_street.setCurrentText(self.street_name)
        self.comboBox_house.setCurrentText(self.house_number)
        self.comboBox_entr.setCurrentText(str(self.num_entr))
        self.lineEdit_floor.setText('' if self.flatfloor==None else str(self.flatfloor))
        self.lineEdit_serKpu.setText('' if self.ser_num_kpu==None else str(self.ser_num_kpu))
        self.lineEdit_serial.setText('' if self.ser_num_pu==None else str(self.ser_num_pu))
        self.lineEdit_flat.setText('' if self.flat==None else str(self.flat))
        self.comboBox_type.setCurrentText(self.type_counter)
        self.label_typeKPU.setText('' if self.type_kpu==None else str(self.type_kpu))
        self.label_dateLast.setText('' if self.last_date==None else str(self.last_date))
        self.label_value.setText('' if self.last_pok==None else str(self.last_pok))
        self.checkBox.setChecked(self.workability)
        self.checkBox_rs485.setChecked(False if self.type_connection == 1 else True)
        self.lineEdit_klemma.setText('' if self.klemma==None else str(self.klemma))
        self.lineEdit_coef.setText('' if self.coefficient==None else str(self.coefficient))
        self.lineEdit_coefons.setText('' if self.consumption_coeff==None else str(self.consumption_coeff))
        self.comboBox_marka.setCurrentText(self.marka)
        if self.id_entr == None: self.checkBox_type.setChecked(False)
        else: self.checkBox_type.setChecked(True)
        if self.date_install == None: 
            self.pushButton_install.show()
            self.dateEdit_install.hide()
            self.label_install.hide()
        else: 
            self.pushButton_install.hide()
            self.dateEdit_install.show()
            self.label_install.show()
            self.dateEdit_install.setDate(self.date_install)
        if self.date_deinstall == None: 
            self.pushButton_deinstall.show()
            self.dateEdit_deinstall.hide()
            self.label_deinstall.hide()
        else: 
            self.pushButton_deinstall.hide()
            self.dateEdit_deinstall.show()
            self.label_deinstall.show()
            self.dateEdit_deinstall.setDate(self.date_deinstall)
        self.dateTimeEdit_dateNew.setDateTime(datetime.datetime.today().replace(minute=0, second=0))
        self.dateEdit_dateInstall.setDate(datetime.date.today())
        self.dateTimeEdit_date.setDateTime(datetime.datetime.today().replace(minute=0, second=0))
        self.dateTimeEdit_start.setDateTime(datetime.datetime.today().replace(minute=0, second=0) - timedelta(days=3))
        self.dateTimeEdit_end.setDateTime(datetime.datetime.today().replace(minute=0, second=0))
        self.label.setText('id_klemma = ' + str(self.id_pu))
    
    def find_counter(self):
        cur = self.conn.cursor()
        counter_query = """SELECT
                            counter.id_klemma, counter.working_capacity
                        FROM
                            cnt.counter"""
        counter_query  = counter_query + " WHERE counter.serial_number = '" + str(self.val_ser_num_pu)+"'"
        cur.execute(counter_query)   
        self.list_counter = cur.fetchall()
        if len(self.list_counter)==0: self.id_pu = 0 
        else: 
            self.id_pu = self.list_counter[0][0]
            self.work = self.list_counter[0][1]
    
    def findFlat(self):
        cur = self.conn.cursor()
        flat_query = """SELECT
                            flat.id_flat, flat.id_entr
                        FROM
                            public.flat
                        left join public.entrance
                            on flat.id_entr = entrance.id_entr"""
        flat_query  = flat_query + " WHERE entrance.id_house = " + str(self.val_id_house) + " AND flat.num_flat = " + str(self.val_flat)
        cur.execute(flat_query)   
        self.list_id_flat = cur.fetchall()
        if len(self.list_id_flat)==0: 
            self.val_id_flat = None
            self.add_flat()
            self.flag_work = False
        else: self.val_id_flat = self.list_id_flat[0][0]
        if self.val_id_entr == None: self.val_id_entr = self.list_id_flat[0][1]
 
    def findKpu(self):
        cur = self.conn.cursor()
        kpu_query = """SELECT
                            kpu.id_kpu, kpu.id_entr, kpu.adress, kpu.type_kpu, kpu.workability
                        FROM
                            cnt.kpu
                        inner join public.flat
                            on flat.id_entr = kpu.id_entr"""
        kpu_query  = kpu_query + " WHERE kpu.ser_num = " + str(self.val_ser_num_kpu)
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
            self.flag_work = False
            self.paint_text(self.label_error,self.text,"red") 
        elif self.list_id_kpu[0][4] == 0:
            self.text = 'Состояние выбранного КПУ - неработоспособен'
            self.flag_work = False
            self.paint_text(self.label_error,self.text,"red") 
        else: 
            self.val_id_kpu = self.list_id_kpu[0][0]
            if self.val_id_entr == None: self.val_id_entr = self.list_id_kpu[0][1]
            self.val_adress = self.list_id_kpu[0][2]
            self.val_type_kpu = self.list_id_kpu[0][3]
    
    def findKpuNew(self):
        cur = self.conn.cursor()
        kpu_query = """SELECT
                            kpu.id_kpu, kpu.adress, kpu.type_kpu, kpu.workability
                        FROM
                            cnt.kpu
                        inner join public.flat
                            on flat.id_entr = kpu.id_entr"""
        kpu_query  = kpu_query + " WHERE kpu.ser_num = " + str(self.val_ser_num_kpu)
        if self.val_id_entr != None:
            kpu_query  = kpu_query + " AND kpu.id_entr = " + str(self.val_id_entr)
            self.text = 'На заданном адресе не установлен данный КПУ'
        else: self.text = 'В БД отсутсвует КПУ с данным серийным номером'    
        cur.execute(kpu_query)
        self.list_id_kpuNew = cur.fetchall()
        if len(self.list_id_kpuNew) == 0: 
            self.flag_workNew = False
            self.paint_text(self.label_error,self.text,"red") 
        elif self.list_id_kpuNew[0][3] == 0:
            self.text = 'Состояние выбранного КПУ - неработоспособен'
            self.flag_workNew = False
            self.paint_text(self.label_error,self.text,"red") 
        else: 
            self.val_id_kpu = self.list_id_kpuNew[0][0]
            self.val_adress = self.list_id_kpuNew[0][1]
            self.val_type_kpu = self.list_id_kpuNew[0][2]
    
    def find_id_entr(self):
        cur = self.conn.cursor()
        entr_query = """SELECT
                         flat.id_entr
                       FROM
                         cnt.counter, public.flat
                       WHERE counter.id_klemma = %s and (flat.id_flat = counter.id_flat or flat.id_entr = counter.id_entr)"""
        cur.execute(entr_query, (self.id_counter,))
        self.list_id_entr = cur.fetchall()
        if len(self.list_id_entr) == 0: 
            QMessageBox.warning(self, 'Внимание', 'Не удалось определить номер подъезда')
            self.flag_workNew = False
        else: 
            self.val_id_entr = self.list_id_entr[0][0]
    
    def find_fdb_counter(self,fireBird):
        try:
            cur = fireBird.cursor()
            if self.type_connection == 1:
                sql_query = """ SELECT ID_KLEMMA FROM COUNTER 
                                WHERE KLEMMA = ? AND 
                                ID_KPU = (SELECT ID_KPU FROM KPU 
                                WHERE TYPE_KPU = ? AND ADRESS = ?)"""
                cur.execute(sql_query, (self.klemma, self.type_kpu, self.adress))
                data = cur.fetchall()
                self.id_klemma_fdb = data[0][0]
            if self.type_connection == 2:
                sql_query = """ SELECT ID_KLEMMA
                                FROM COUNTER
                            WHERE SER_NUM=?"""
                cur.execute(sql_query, (self.ser_num_pu, ))
                data = cur.fetchall()
                self.id_klemma_fdb = data[0][0]
            cur.close()
        except:
            print (traceback.format_exc())

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
    
    def insert_start_value(self):
        cur = self.conn.cursor()
        sql_query = """INSERT INTO cnt.start_value(id_klemma, date_val, st_value, impulse_value)                                                                                             
                    VALUES (%s, %s, %s, %s)"""
        cur.execute(sql_query, (self.id_pu, self.date_val, self.st_value, self.impulse_value)) 
        self.conn.commit()
        cur.close()  
    
    def insert_counter(self):
        cur = self.conn.cursor()
        sql_query = """INSERT INTO cnt.counter(klemma, id_kpu, id_entr, id_flat, 
                        id_marka, coefficient, serial_number, working_capacity, 
                        date_install, id_house, type_counter, consumption_coeff, type_connection)                                                                                             
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_klemma;"""
        cur.execute(sql_query, (self.val_klemma, self.val_id_kpu, self.val_id_entr, self.id_flat, 
                    self.val_id_marka, self.val_coefficient, self.val_ser_num_pu, self.val_workability,
                    self.val_date_install, self.id_house, self.id_type_counter, self.val_consumption_coeff, self.val_rs485)) 
        self.conn.commit()
        data = cur.fetchall()
        cur.close()
        self.id_pu=data[0][0]
        print(self.id_pu)
        #self.label.setText('id_klemma = ' + str(self.id_pu))

    def insert_flat(self):
        self.val_id_entr = int(self.list_id_entrance[self.comboBox_entrAdd.currentIndex()])
        self.val_comment = self.lineEdit_noteAdd.text()
        if self.val_comment == '': self.val_comment = None
        self.val_flatfloor = self.lineEdit_floorAdd.text()
        self.val_flatfloor = None if self.val_flatfloor == '' else int(self.val_flatfloor)
        cur = self.conn.cursor()
        sql_query = """INSERT INTO public.flat(id_entr, num_flat, fio, flatfloor)                                                                                             
                    VALUES (%s, %s, %s, %s) RETURNING id_flat;"""
        cur.execute(sql_query, (self.val_id_entr, self.val_flat, self.val_comment, self.val_flatfloor)) 
        self.conn.commit()
        data = cur.fetchall()
        self.val_id_flat = data[0][0]
        cur.close()
        self.cansel() 
    
    def insert_fdb(self,fireBird):
        try:
            if self.val_rs485 == 1:
                sql_query = """ SELECT ID_KPU FROM KPU 
                                WHERE TYPE_KPU = ? AND ADRESS = ? """
                cur = fireBird.cursor()
                cur.execute(sql_query, (self.val_type_kpu, self.val_adress))
                data = cur.fetchall()
                self.id_kpu_fdb = data[0][0]
                sql_query = """ INSERT INTO COUNTER(KLEMMA, ID_KPU, TYPE_COUNTER)
                                VALUES (?, ?, ?) """
                cur.execute(sql_query, (self.val_klemma, self.id_kpu_fdb, self.val_type_counter))
                self.conn.commit()
                cur.close()
            if self.val_rs485 == 2:
                sql_query = """ INSERT INTO COUNTER(TYPE_COUNTER, SER_NUM)
                                VALUES (?, ?) """
                cur = fireBird.cursor()
                cur.execute(sql_query, (self.val_type_counter, self.val_ser_num_pu))
                self.conn.commit()
                cur.close()
        except:
            print (traceback.format_exc())
    
    def insert_counter_replace(self):
        cur = self.conn.cursor()
        sql_query = """INSERT INTO cnt.counter_replace(id_old_counter, id_new_counter, date_replace)
                        VALUES (%s, %s, %s)"""
        cur.execute(sql_query, (self.id_counter, self.id_pu, self.val_date_install)) 
        self.conn.commit()
        cur.close()
    
    def open_replace(self):
        try:
            self.resize(900,350)
            self.widget_puNew.show()
            self.label_errorNew.hide()
            self.label_error.hide()
            self.tabWidget.setCurrentIndex(2)
            self.pushButton_save.setEnabled(False)
            self.pushButton_replace.setEnabled(False)
            self.pushButton_addStart.setEnabled(False)
            self.lineEdit_serKpuNew.setText('' if self.ser_num_kpu==None else str(self.ser_num_kpu))
            self.lineEdit_klemmaNew.setText('' if self.klemma==None else str(self.klemma))
            self.lineEdit_coefNew.setText('' if self.coefficient==None else str(self.coefficient))
            self.lineEdit_coefonsNew.setText('' if self.consumption_coeff==None else str(self.consumption_coeff))
            self.comboBox_markaNew.setCurrentText(self.marka)
            self.checkBox.setChecked(False)
            self.checkBox_rs485New.setChecked(False if self.type_connection == 1 else True)
            if self.tableWidget_dateVal.rowCount() > 0 and self.tableWidget_dateVal.item(0,2).text()!='': self.spinBox_impNew.setValue(float(self.tableWidget_dateVal.item(0,2).text()))
        except:
            print (traceback.format_exc())
            
    def paint_text(self,name_label,text,color_text):
        pal = name_label.palette()
        pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor(color_text))
        name_label.setPalette(pal)
        #self.resize(self.label_error.sizeHint())
        name_label.setText(text)
        name_label.show()
   
    def replace_counter(self):
        try:
            self.label_errorNew.hide()
            self.lineEdit_serKpuNew.setStyleSheet('background : #FFFFFF;')
            self.lineEdit_serialNew.setStyleSheet('background : #FFFFFF;')
            self.lineEdit_klemmaNew.setStyleSheet('background : #FFFFFF;')
            self.lineEdit_coefNew.setStyleSheet('background : #FFFFFF;')
            self.flag_workNew = True
            flag = False
            text='Введено некорректное значение'
            self.val_ser_num_kpu = self.lineEdit_serKpuNew.text()
            if self.val_ser_num_kpu == '': self.val_ser_num_kpu = None
            self.val_klemma = str(self.lineEdit_klemmaNew.text())
            self.val_klemma = None if self.val_klemma == '' else int(self.val_klemma)
            self.val_coefficient = str(self.lineEdit_coefNew.text())
            self.val_coefficient = None if self.val_coefficient == '' else int(self.val_coefficient)
            self.val_consumption_coeff = str(self.lineEdit_coefonsNew.text())
            self.val_consumption_coeff = 1 if self.val_consumption_coeff == '' else int(self.val_consumption_coeff)
            self.val_id_marka = int(self.list_id_marka[self.comboBox_markaNew.currentIndex()])
            if self.val_id_marka == 0: self.val_id_marka = None
            self.val_date_install = self.dateEdit_dateInstall.date().toString("yyyy-MM-dd")
            self.val_start_date = self.dateTimeEdit_dateNew.dateTime().toString("yyyy-MM-dd hh:mm:00")
            self.val_note = str(self.textEdit_noteNew.toPlainText())
            self.val_workability = self.checkBoxNew.isChecked()
            self.val_rs485 = 2 if self.checkBox_rs485New.isChecked() else 1 
            self.val_st_value = self.checkBox_startZn.isChecked()
            self.val_ser_num_pu = str(self.lineEdit_serialNew.text())
            if self.val_ser_num_pu == '': self.val_ser_num_pu = None
            if self.val_workability:
                if self.val_rs485==False:
                    if self.val_ser_num_kpu == None:
                        self.lineEdit_serKpuNew.setStyleSheet('background : #FDDDE6;')
                        self.flag_workNew = False
                    if self.val_klemma == None:
                        self.lineEdit_klemmaNew.setStyleSheet('background : #FDDDE6;')
                        self.flag_workNew = False
                    if self.val_coefficient == None:
                        self.lineEdit_coefNew.setStyleSheet('background : #FDDDE6;')
                        self.flag_workNew = False
                if self.val_rs485:
                    if self.val_ser_num_pu == None:
                        self.lineEdit_serialNew.setStyleSheet('background : #FDDDE6;')
                        self.flag_workNew = False
            if self.val_ser_num_pu != None: 
                self.find_counter()
                if self.id_pu != 0 and self.work == True:
                    self.select()
                    text='ПУ с серийным номером '+str(self.val_ser_num_pu)+' уже используется. Город '+str(self.city_name)+', улица '+str(self.street_name)+', дом '+str(self.house_number)+', квартира '+str(self.flat)+', серийный номер КПУ = '+str(self.ser_num_kpu)
                    QMessageBox.warning(self, 'Внимание', text)
                    self.flag_workNew = False
                if self.id_pu != 0 and self.work == False:
                    self.select()
                    text='ПУ с серийным номером '+str(self.val_ser_num_pu)+' имеется в БД. Город '+str(self.city_name)+', улица '+str(self.street_name)+', дом '+str(self.house_number)+', квартира '+str(self.flat)+', серийный номер КПУ = '+str(self.ser_num_kpu)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Внимание")
                    msg.setText(text)
                    msg.setInformativeText('Хотите продолжить замену?')
                    okButton = msg.addButton('Окей', QMessageBox.AcceptRole)
                    msg.addButton('Отмена', QMessageBox.RejectRole)
                    msg.exec()
                    if msg.clickedButton() == okButton:
                        flag = True
                    else: self.flag_workNew = False
            self.find_id_entr()        
            if self.val_ser_num_kpu != None: self.findKpuNew()
            else: self.val_id_kpuNew = None
            if self.flag_workNew:
                self.update_off()
                self.select_parameters_firebird()
                self.create_connection_firebird()
                if self.val_workability: 
                    self.find_fdb_counter(self.connection)
                    self.update_fdb(self.connection)
                else: self.deleted_fdb(self.connection) 
                if flag == True: self.update_replace()
                else: self.insert_counter()
                if self.val_note != '': self.update_counter_history()
                self.insert_counter_replace()
                if self.val_st_value:
                    self.date_val = self.val_start_date
                    self.st_value = self.doubleSpinBox_valNew.value()
                    self.impulse_value = self.spinBox_impNew.value()
                    self.insert_start_value()
                self.canselNew()
                self.id_counter=self.id_pu
                self.paint_text(self.label_error,'ПУ успешно заменен',"green")
                self.select()
                self.filling()
                self.tabWidget.setCurrentIndex(0)
                self.select_start_value()
                self.select_history()
                self.show_value()
        except :
            print (traceback.format_exc())
            self.paint_text(self.label_error,self.text,"red")
    
    def select(self):
        cur = self.conn.cursor()
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
                          counter.last_date, counter.id_entr, counter.id_kpu,
                          counter.id_flat, counter.id_house, counter.type_counter,
                          counter.type_connection, kpu.adress
                        FROM
                          cnt.counter
                          left join public.flat
                            on flat.id_flat = counter.id_flat
                          left join public.entrance
                            on entrance.id_entr = flat.id_entr     
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
                        WHERE counter.id_klemma = %s 
                        AND counter.id_flat is not null
                        UNION
                        SELECT  			 			
                          counter.consumption_coeff, city.city_name,
                          street.street_name, house.house_number,
                          entrance.num_entr, null, null,
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
                          counter.last_date, counter.id_entr, counter.id_kpu, null,
                          counter.id_house, counter.type_counter, 
                          counter.type_connection, kpu.adress
                        FROM
                          cnt.counter 
                          left join cnt.kpu
                            on counter.id_kpu=kpu.id_kpu
                          left join public.entrance
                            on entrance.id_entr = kpu.id_entr  
                          left join cnt.marka
                            on counter.id_marka = marka.id_marka
                          left join public.house
                            on house.id_house = entrance.id_house
                          left join public.street
                            on street.id_street = house.id_street
                          left join public.city
                            on city.id_city = street.id_city
                        WHERE counter.id_klemma = %s
                        AND counter.id_flat is null"""              
        cur.execute(self.sql_query, (self.id_pu, self.id_pu))
        data = cur.fetchall()
        cur.close()
        self.consumption_coeff = data[0][0]
        self.city_name = data[0][1]
        self.street_name = data[0][2]
        self.house_number = data[0][3]
        self.num_entr = data[0][4]
        self.flatfloor = data[0][5]
        self.flat = data[0][6]
        self.type_counter = data[0][7]
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
        self.id_entr = data[0][19]
        self.id_kpu = data[0][20]
        self.id_flat = data[0][21]
        self.id_house = data[0][22]
        self.id_type_counter = data[0][23]
        self.type_connection = data[0][24]
        self.adress = data[0][25]
    
    def select_start_value(self):
        start_value_query ="""SELECT date_val, st_value, impulse_value
                                FROM cnt.start_value"""
        start_value_query = start_value_query + " WHERE id_klemma = " + str(self.id_counter)
        cur = self.conn.cursor()
        cur.execute(start_value_query) 
        data = cur.fetchall()
        cur.close() 
        self.tableWidget_stZn.setRowCount(0)
        for index,row in enumerate(data):
            self.tableWidget_stZn.insertRow(0)
            for k in range(len(row)):
                    item = QTableWidgetItem('' if data[index][k]==None else str(data[index][k]))                 
                    self.tableWidget_stZn.setItem(0,k,item)
        self.tableWidget_stZn.resizeColumnsToContents()
    
    def save_start_value(self):
        self.id_pu = self.id_counter()
        self.date_val = self.dateTimeEdit_date.dateTime().toString("yyyy-MM-dd hh:mm:00")
        self.st_value = self.doubleSpinBox_val.value()
        self.impulse_value = self.spinBox_imp.value()
        self.insert_start_value()
        self.select_start_value()
    
    def select_date_install(self):
        self.pushButton_install.hide()
        self.dateEdit_install.show()
        self.label_install.show()
        self.dateEdit_install.setDate(datetime.date.today())

    def select_date_deinstall(self):
        self.pushButton_deinstall.hide()
        self.dateEdit_deinstall.show()
        self.label_deinstall.show()
        self.dateEdit_deinstall.setDate(datetime.date.today()) 
    
    def select_impulse(self):
        self.label_errorNew.hide()
        date_value_query ="""SELECT impulse_value
                                FROM cnt.date_value"""
        date_value_query = date_value_query + " WHERE id_klemma = " + str(self.id_counter) + " AND date_val = '" + self.dateTimeEdit_dateNew.dateTime().toString("yyyy-MM-dd hh:mm:00") +"'"
        cur = self.conn.cursor()
        cur.execute(date_value_query) 
        data = cur.fetchall()
        cur.close()
        if len(data)==0:
            self.paint_text(self.label_errorNew,'Отсутствуют данные на выбранную дату',"red")
        else: self.spinBox_impNew.setValue(data[0][0])
  
    def select_parameters_firebird(self):
        sql_query = """SELECT ip_rassbery, fdb_login, fdb_password, fdb_path
                       FROM save.login_data
                       WHERE id_entr = %s"""
        cur = self.conn.cursor()
        cur.execute(sql_query, (self.val_id_entr, ))
        data = cur.fetchall()
        cur.close()
        self.ip_rassbery = data[0][0]
        self.fdb_login = data[0][1]
        self.fdb_password = data[0][2]
        self.fdb_path = data[0][3]
     
    def select_history(self):
        self.tableWidget_history.setRowCount(0)       
        self.sql_query = """SELECT city.city_name, street.street_name,
                                   house.house_number, entrance.num_entr,
                                   flat.num_flat, kpu.ser_num,
                                   counter_history.klemma, counter_history.working_capacity,
                                   counter_history.date_change, counter_history.date_deinstall,
                                   counter_history.note
                            FROM
                              cnt.counter
                              inner join cnt.counter_history
                                on counter_history.id_klemma = counter.id_klemma
                              inner join cnt.kpu
                                on kpu.id_kpu = counter_history.id_kpu
                              inner join public.flat
                                on flat.id_flat = counter_history.id_flat
                              left join public.entrance
                                on entrance.id_entr = flat.id_entr
                              left join public.house
                                on house.id_house = entrance.id_house
                              left join public.street
                                on street.id_street = house.id_street
                              left join public.city
                                on city.id_city = street.id_city
                            WHERE counter.id_klemma = %s AND counter.id_flat is not null
                            UNION
                            SELECT city.city_name, street.street_name,
                                   house.house_number, entrance.num_entr,
                                   null, kpu.ser_num,
                                   counter_history.klemma, counter_history.working_capacity,
                                   counter_history.date_change, counter_history.date_deinstall,
                                   counter_history.note
                            FROM
                              cnt.counter
                              inner join cnt.counter_history
                                on counter_history.id_klemma = counter.id_klemma
                              inner join cnt.kpu
                                on kpu.id_kpu = counter_history.id_kpu
                              left join public.entrance
                                on entrance.id_entr = counter_history.id_entr
                              left join public.house
                                on house.id_house = counter_history.id_house
                              left join public.street
                                on street.id_street = house.id_street
                              left join public.city
                                on city.id_city = street.id_city
                            WHERE counter.id_klemma = %s AND counter.id_flat is null"""
        cur = self.conn.cursor()
        cur.execute(self.sql_query, (self.id_counter,self.id_counter))   
        data = cur.fetchall()
        for index,row in enumerate(data):
            self.tableWidget_history.insertRow(0)
            for k in range(len(row)):
                    item = QTableWidgetItem('' if data[index][k]==None else str(data[index][k]))                 
                    self.tableWidget_history.setItem(0,k,item)                 
        cur.close()    
        self.tableWidget_history.resizeColumnsToContents()
    
    def show_value(self):
        date_start = self.dateTimeEdit_start.dateTime().toString("yyyy-MM-dd hh:mm:00")
        date_end = self.dateTimeEdit_end.dateTime().toString("yyyy-MM-dd hh:mm:00")
        date_value_query ="""SELECT value_zn, date_val, impulse_value, calculate_error, empty, line_state
                                FROM cnt.date_value"""
        date_value_query = date_value_query + " WHERE id_klemma = " + str(self.id_counter) + " AND date_val > '" + date_start + "' AND date_val < '" + date_end + "';"
        cur = self.conn.cursor()
        cur.execute(date_value_query) 
        data = cur.fetchall()
        cur.close() 
        self.tableWidget_dateVal.setRowCount(0)
        for index,row in enumerate(data):
            self.tableWidget_dateVal.insertRow(0)
            for k in range(len(row)):
                    item = QTableWidgetItem('' if data[index][k]==None else str(data[index][k]))                 
                    self.tableWidget_dateVal.setItem(0,k,item)
        self.tableWidget_dateVal.resizeColumnsToContents()
 
    def update_off(self):
        cur = self.conn.cursor()
        sql_query = """ UPDATE cnt.counter
                        SET working_capacity=False, date_deinstall=%s
                        WHERE id_klemma=%s"""
        cur.execute(sql_query, (self.val_date_install, self.id_counter))               
        self.conn.commit()
        cur.close()
    
    def update_replace(self):
        cur = self.conn.cursor() 
        sql_query = """ UPDATE cnt.counter
                        SET klemma=%s, id_kpu=%s, id_entr=%s, id_flat=%s, working_capacity=%s, 
                        date_install=%s, date_deinstall=null, id_house=%s, type_connection=%s
                        WHERE id_klemma=%s"""
        cur.execute(sql_query, (self.val_klemma, self.val_id_kpu, self.val_id_entr, self.id_flat, 
            self.val_workability, self.val_date_install, self.id_house, self.val_rs485, self.id_pu)) 
        self.conn.commit()    
        cur.close()

    def update_counter_history(self):
        cur = self.conn.cursor()
        sql_query = """ UPDATE cnt.counter_history
                        SET note = %s
                        WHERE id =(SELECT MAX(id)
                                   FROM cnt.counter_history
                                   WHERE id_klemma = %s)"""
        cur.execute(sql_query, (self.val_note, self.id_pu))       
        self.conn.commit()
        cur.close()
 
    def update_fdb(self,fireBird):
        try:
            if self.val_rs485 == 1:
                if self.val_ser_num_kpu != self.ser_num_kpu :
                    sql_query = """ SELECT ID_KPU FROM KPU 
                                    WHERE TYPE_KPU = ? AND ADRESS = ? """
                    cur = fireBird.cursor()
                    cur.execute(sql_query, (self.val_type_kpu, self.val_adress))
                    data = cur.fetchall()
                    self.id_kpu_fdb = data[0][0]
                    sql_query = """ UPDATE COUNTER
                                    SET ID_KPU=?
                                WHERE ID_KLEMMA=?"""
                    cur.execute(sql_query, (self.id_kpu_fdb, self.id_klemma_fdb)) 
                    self.conn.commit()
                    cur.close()
                if self.val_klemma != self.klemma :
                    sql_query = """ UPDATE COUNTER
                                    SET KLEMMA = ?
                                WHERE ID_KLEMMA=?"""
                    cur = fireBird.cursor()
                    cur.execute(sql_query, (self.val_klemma, self.id_klemma_fdb)) 
                    self.conn.commit()
                    cur.close() 
                if self.type_connection == 2:
                    sql_query = """ UPDATE COUNTER
                                    SET SER_NUM=?
                                WHERE ID_KLEMMA=?"""
                    cur = fireBird.cursor() 
                    cur.execute(sql_query, (self.val_ser_num_pu, self.id_klemma_fdb)) 
                    self.conn.commit()
                    cur.close()
            if self.val_rs485 == 2:
                if self.val_ser_num_pu != self.ser_num_pu:
                    sql_query = """ UPDATE COUNTER
                                    SET SER_NUM=?
                                WHERE ID_KLEMMA=?"""
                    cur = fireBird.cursor()
                    cur.execute(sql_query, (self.val_ser_num_pu, self.id_klemma_fdb))
                    self.conn.commit()
                    cur.close()
                if self.type_connection == 1:
                    sql_query = """ UPDATE COUNTER
                                    SET KLEMMA=NULL, ID_KPU=NULL
                                WHERE ID_KLEMMA=?"""
                    cur = fireBird.cursor()            
                    cur.execute(sql_query, (self.id_klemma_fdb,)) 
                    self.conn.commit()
                    cur.close()
        except:
            print (traceback.format_exc())
    
    def update(self):
        if not self.val_house_counter: 
            self.val_id_entr = None
            self.val_id_house = None
        cur = self.conn.cursor()
        sql_query = """ UPDATE cnt.counter
                        SET klemma=%s, id_kpu=%s, id_entr=%s, id_flat=%s, id_marka=%s, 
                        coefficient=%s, serial_number=%s, working_capacity=%s, date_install=%s, 
                        date_deinstall=%s, id_house=%s, type_counter=%s, consumption_coeff=%s, type_connection=%s
                        WHERE id_klemma=%s"""
        cur.execute(sql_query, (self.val_klemma, self.val_id_kpu, self.val_id_entr, self.val_id_flat, 
            self.val_id_marka, self.val_coefficient, self.val_ser_num_pu, self.val_workability, self.val_date_install, 
            self.val_date_deinstal, self.val_id_house, self.val_type_counter, self.val_consumption_coeff, self.val_rs485, self.id_pu))               
        self.conn.commit()
        cur.close()
     
    def verify(self):
        try:
            self.label_error.hide()
            self.lineEdit_serial.setStyleSheet('background : #FFFFFF;')
            self.lineEdit_serKpu.setStyleSheet('background : #FFFFFF;')
            self.lineEdit_klemma.setStyleSheet('background : #FFFFFF;')
            self.comboBox_city.setStyleSheet('background : #FFFFFF;')
            self.lineEdit_coef.setStyleSheet('background : #FFFFFF;')
            self.comboBox_street.setStyleSheet('background : #FFFFFF;')
            self.comboBox_house.setStyleSheet('background : #FFFFFF;')
            self.comboBox_entr.setStyleSheet('background : #FFFFFF;')
            self.flag_work = True
            text='Введено некорректное значение'  
            self.val_ser_num_kpu = None if self.lineEdit_serKpu.text() == '' else int(self.lineEdit_serKpu.text())
            if self.comboBox_house.currentText() != '': self.val_id_house = int(self.list_id_house[self.comboBox_house.currentIndex()])
            else: self.val_id_house = None 
            self.val_street = self.comboBox_street.currentText()
            self.val_city = self.comboBox_city.currentText()
            self.val_house = self.comboBox_city.currentText()
            self.val_entr = str(self.comboBox_entr.currentText())
            if self.val_entr != '': self.val_id_entr = int(self.list_id_entrance[self.comboBox_entr.currentIndex()])
            else: self.val_id_entr = None
            self.val_floor = str(self.lineEdit_floor.text())
            self.val_floor = None if self.val_floor == '' else int(self.val_floor)
            self.val_flat = None if self.lineEdit_flat.text() == '' else int(self.lineEdit_flat.text())
            self.val_type_counter = int(self.comboBox_type.currentIndex())
            if self.val_type_counter == 0: self.val_type_counter = None
            self.val_klemma = str(self.lineEdit_klemma.text())
            self.val_klemma = None if self.val_klemma == '' else int(self.val_klemma)
            self.val_ser_num_pu = str(self.lineEdit_serial.text())
            if self.val_ser_num_pu == '': self.val_ser_num_pu = None
            self.val_coefficient = str(self.lineEdit_coef.text())
            self.val_coefficient = None if self.val_coefficient == '' else int(self.val_coefficient)
            self.val_consumption_coeff = str(self.lineEdit_coefons.text())
            self.val_consumption_coeff = 1 if self.val_consumption_coeff == '' else int(self.val_consumption_coeff)
            self.val_id_marka = int(self.list_id_marka[self.comboBox_marka.currentIndex()])
            if self.val_id_marka == 0: self.val_id_marka = None
            self.val_date_install = self.dateEdit_install.date().toString("yyyy-MM-dd")
            if self.val_date_install == '1752-09-14': self.val_date_install = None
            self.val_date_deinstal = self.dateEdit_deinstall.date().toString("yyyy-MM-dd")
            if self.val_date_deinstal == '9999-12-31': self.val_date_deinstal = None
            self.val_house_counter = self.checkBox_type.isChecked()
            self.val_workability = self.checkBox.isChecked()
            self.val_rs485 = 1 if self.checkBox_rs485.isChecked() == False else 2
            if self.val_workability:
                if self.val_rs485 == 1:
                    if self.val_ser_num_kpu == None: 
                        self.lineEdit_serKpu.setStyleSheet('background : #FDDDE6;')
                        self.flag_work = False
                    if self.val_klemma == None:
                        self.lineEdit_klemma.setStyleSheet('background : #FDDDE6;')
                        self.flag_work = False
                    if self.val_coefficient == None:
                        self.lineEdit_coef.setStyleSheet('background : #FDDDE6;')
                        self.flag_work = False
                if self.val_rs485 == 2:
                    if self.val_ser_num_pu == None:
                        self.lineEdit_serial.setStyleSheet('background : #FDDDE6;')
                        self.flag_work = False
                    if self.val_id_entr == None and self.val_flat == None:
                        self.paint_text(self.label_error,'Введите номер подъезда или номер квартиры',"red")
                        self.flag_work = False
            if self.val_flat != None:
                if self.val_city == '':
                    self.comboBox_city.setStyleSheet('background : #FDDDE6;')
                    self.flag_work = False
                if self.val_street == '':
                    self.comboBox_street.setStyleSheet('background : #FDDDE6;')
                    self.flag_work = False
                if self.val_house == '':
                    self.comboBox_house.setStyleSheet('background : #FDDDE6;')
                    self.flag_work = False
                else: self.findFlat()
            else: self.val_id_flat = None  
            if self.val_ser_num_kpu != None: self.findKpu()
            else: self.val_id_kpu = None
            if self.flag_work:
                if self.val_workability != self.workability or (self.val_workability == True and (self.val_klemma != self.klemma or self.val_type_counter != self.id_type_counter or (self.val_rs485 == True and self.val_ser_num_pu != self.ser_num_pu) or (self.val_rs485 == False and self.val_ser_num_kpu != self.ser_num_kpu))):
                    self.select_parameters_firebird()
                    self.create_connection_firebird()
                    if self.workability==True and self.val_workability==False:
                        self.find_fdb_counter(self.connection)
                        self.deleted_fdb(self.connection)
                    elif self.workability==False and self.val_workability==True: 
                        self.insert_fdb(self.connection)    
                    else:
                        self.find_fdb_counter(self.connection)
                        self.update_fdb(self.connection)
                    self.connection.close()
                self.update()
                #self.label.setText('id_klemma = ' + str(self.id_klemma))
                self.select()
                self.filling()
                QMessageBox.information(self, 'Информация', 'Данные о ПУ сохранены')
        except: 
            print (traceback.format_exc())
            self.paint_text(self.label_error,self.text,"red") 
   