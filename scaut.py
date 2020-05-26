import sys
import psycopg2
import traceback
import scaut_ui, add_scaut_ui, kpu
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QTableWidgetItem
from PyQt5.QtGui import *
from PyQt5.Qt import *

class Scaut(QtWidgets.QWidget, scaut_ui.Ui_Form):
    def __init__(self, conn):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('СКАУТ')      
        self.conn = conn
        self.pushButton_add.clicked.connect(self.add_window)
        self.tableWidget_scaut.doubleClicked.connect(self.cell_was_clicked)
        self.pushButton_filtr.clicked.connect(self.select)
        self.tableWidget_scaut.horizontalHeader().hideSection(4)
        self.select()
        self.filtr_city()
        self.comboBox_city.currentIndexChanged.connect(self.filtr_street)
        self.comboBox_city.setCurrentText('Обнинск')
        self.comboBox_street.currentIndexChanged.connect(self.filtr_house)
        self.comboBox_street.setCurrentText('Поленова')
        self.comboBox_house.currentIndexChanged.connect(self.filtr_entrance)
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
        self.list_id_street = [0]
        for index,row in enumerate(data):   
            self.list_id_street.append(data[index][1])
            self.comboBox_street.addItem(str(data[index][0]))    
        cur.close()  
        
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
        
    def select(self):
        self.tableWidget_scaut.setRowCount(0)
        self.sql_query = """SELECT
                                city.city_name,	
                                street.street_name,
                                house.house_number,
                                entrance.num_entr,
                                entrance.id_entr                               
                            FROM
                                public.entrance
                            left join public.house
                                on house.id_house = entrance.id_house
                            left join public.street
                                on street.id_street = house.id_street
                            left join public.city
                                on city.id_city = street.id_city"""     
        if self.comboBox_city.currentText()!='':
            if self.comboBox_street.currentText()!='':
                if self.comboBox_house.currentText()!='':
                    if self.comboBox_entrance.currentText()!='':
                        self.sql_query = self.sql_query + " WHERE entrance.id_entr = " + str(self.list_id_entrace[self.comboBox_entrance.currentIndex()])
                    else:                    
                        self.sql_query = self.sql_query + " WHERE house.id_house = " + str(self.list_id_house[self.comboBox_house.currentIndex()])
                else:
                    self.sql_query = self.sql_query + " WHERE street.id_street = " + str(self.list_id_street[self.comboBox_street.currentIndex()]) 
            else:   
                self.sql_query = self.sql_query + " WHERE city.id_city = " + str(self.list_id_city[self.comboBox_city.currentIndex()]) 
        self.sql_query = self.sql_query + " ORDER BY city.city_name DESC, street.street_name DESC, cast(substring(house.house_number from \'^[0-9]+\') as integer) DESC, cast(entrance.num_entr as integer) DESC"      
        cur = self.conn.cursor()
        cur.execute(self.sql_query)        
        data = cur.fetchall()
        for index,row in enumerate(data):
            self.tableWidget_scaut.insertRow(0)
            for k in range(len(row)):
#                item = QTableWidgetItem(str(data[index][k]))
                item = QTableWidgetItem('' if data[index][k]==None else str(data[index][k]))
                self.tableWidget_scaut.setItem(0,k,item)        
        cur.close()
        self.tableWidget_scaut.setMouseTracking(True)
        self.current_hover = 0
        self.tableWidget_scaut.cellEntered.connect(self.line_selection)
        
    def line_selection(self, row, column):
        if self.current_hover != row:
            for j in range(self.tableWidget_scaut.columnCount()):
                self.tableWidget_scaut.item(self.current_hover, j).setBackground(QBrush(QColor('white')))
                self.tableWidget_scaut.item(row, j).setBackground(QBrush(QColor('lightGray')))
        self.current_hover = row
        
    def add_window(self):
        self.add_scaut = Add_Scaut('-1', self.conn)

    def cell_was_clicked(self, coords):
        id_scaut=self.tableWidget_scaut.item(coords.row(), 4).text()
        self.add_scaut = Add_Scaut(id_scaut, self.conn)    

class Add_Scaut(QtWidgets.QWidget, add_scaut_ui.Ui_Form):
    def __init__(self, id_scaut, conn):
        try:
            super().__init__()
            self.setupUi(self)
            self.id_scaut = id_scaut 
            self.label_error.hide()
            self.conn = conn 
            self.filtr_city()
            self.comboBox_city.currentIndexChanged.connect(self.filtr_street)
            self.comboBox_street.currentIndexChanged.connect(self.filtr_house)
            self.lineEdit_port.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
            self.lineEdit_name.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
            self.pushButton_save.clicked.connect(self.verify)
            self.pushButton_kpu.clicked.connect(self.open_kpu)
            if self.id_scaut=='-1':
                self.setWindowTitle('Добавить СКАУТ')
                self.pushButton_kpu.hide()
                self.comboBox_city.setCurrentText('Обнинск')
            if self.id_scaut!='-1':      
                self.setWindowTitle('Информация о  СКАУТ')
                self.pushButton_kpu.show()
                self.select()
                self.filling()
            self.show()
        except :
            print (traceback.format_exc())
            
    def select(self):
        sql_query = """SELECT
                                city.city_name,	
                                street.street_name,
                                house.house_number,
                                entrance.num_entr,
                                login_data.login_user,
                                login_data.pwd_user,   
                                login_data.ip_rassbery,
                                login_data.port_rassbery,
                                entrance.id_entr,
                                login_data.fdb_login,
                                login_data.fdb_password,
                                login_data.fdb_path,
                                login_data.version_fdb
                            FROM
                                save.login_data, public.entrance
                            left join public.house
                                on house.id_house = entrance.id_house
                            left join public.street
                                on street.id_street = house.id_street
                            left join public.city
                                on city.id_city = street.id_city
                            WHERE entrance.id_entr = %s and login_data.id_entr = %s"""
        cur = self.conn.cursor()
        cur.execute(sql_query, (self.id_scaut, self.id_scaut)) 
        data = cur.fetchall()
        cur.close()
        self.city_name = data[0][0]
        self.street_name = data[0][1]
        self.house_number = data[0][2] 
        self.num_entr = data[0][3]
        self.login_user = data[0][4]
        self.pwd_user = data[0][5]
        self.ip_rassbery = data[0][6]
        self.port_rassbery = data[0][7]
        self.id_entr = data[0][8]
        self.fdb_login = data[0][9]
        self.fdb_password = data[0][10]
        self.fdb_path = data[0][11]
        self.version_fdb = data[0][12]
    
    def filling(self):
        self.comboBox_city.setCurrentText(self.city_name)
        #self.comboBox_city.model().item(0).setEnabled(False)
        self.comboBox_street.setCurrentText(self.street_name)
        #self.comboBox_street.model().item(0).setEnabled(False)
        self.comboBox_house.setCurrentText(self.house_number)
        #self.comboBox_house.model().item(0).setEnabled(False)
        self.id_house = int(self.list_id_house[self.comboBox_house.currentIndex()])
        self.spinBox_entr.setValue(self.num_entr)
        self.lineEdit_login.setText(self.login_user)
        self.lineEdit_pasw.setText(self.pwd_user)
        self.lineEdit_host.setText(self.ip_rassbery)
        self.lineEdit_port.setText('' if self.port_rassbery==None else str(self.port_rassbery))
        self.label.setText('id_entr = '+str(self.id_entr))
        self.lineEdit_fdbLogin.setText(self.fdb_login)
        self.lineEdit_fdbPasw.setText(self.fdb_password)
        self.lineEdit_fdbName.setText(self.fdb_path)
        self.lineEdit_name.setText('' if self.version_fdb==None else str(self.version_fdb))
    
    def verify(self):
        try:
            text='Введено некорректное значение'
            if self.comboBox_house.currentText()=='':
                self.comboBox_house.setStyleSheet('background : #FDDDE6;')
                flag_city = False
            else:
                self.comboBox_house.setStyleSheet('background : #FFFFFF;')
                flag_city = True
            if self.comboBox_street.currentText()=='': 
                self.comboBox_street.setStyleSheet('background : #FDDDE6;')
            else:
                self.comboBox_street.setStyleSheet('background : #FFFFFF;')
            if self.comboBox_city.currentText()=='': 
                self.comboBox_city.setStyleSheet('background : #FDDDE6;')
            else:
                self.comboBox_city.setStyleSheet('background : #FFFFFF;')
            self.val_id_house = int(self.list_id_house[self.comboBox_house.currentIndex()])
            self.val_num_entr = int(self.spinBox_entr.value())
            self.val_ip_rassbery = None if self.lineEdit_host.text() == '' else str(self.lineEdit_host.text())
            self.val_port_rassbery = None if self.lineEdit_port.text() == '' else int(self.lineEdit_port.text())
            self.val_login_user = None if self.lineEdit_login.text() == '' else str(self.lineEdit_login.text())
            self.val_pwd_user = None if self.lineEdit_pasw.text() == '' else str(self.lineEdit_pasw.text())
            self.val_fdb_login = None if self.lineEdit_fdbLogin.text() == '' else str(self.lineEdit_fdbLogin.text())
            self.val_fdb_password = None if self.lineEdit_fdbPasw.text() == '' else str(self.lineEdit_fdbPasw.text())
            self.val_fdb_path = None if self.lineEdit_fdbName.text() == '' else str(self.lineEdit_fdbName.text())
            self.val_version_fdb = None if self.lineEdit_name.text() == '' else int(self.lineEdit_name.text())
            if self.id_scaut=='-1' and flag_city==True:
                self.insert()
                QMessageBox.information(self, 'Информация', 'Оборудование успешно добавлено')
                self.label.setText('id_entr = '+str(self.id_entr))
                self.setWindowTitle('Информация о СКАУТ')
                self.pushButton_kpu.show()
            if self.id_scaut!='-1' and flag_city==True:
                self.update()
                pal = self.label_error.palette()
                pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("green"))
                self.label_error.setPalette(pal)
                self.label_error.setText('Данные успешно сохранены')
                self.label_error.show()
        except ValueError:                         
            pal = self.label_error.palette()
            pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
            self.label_error.setPalette(pal)
            self.label_error.setText(text)     
            self.label_error.show() 
 #          QMessageBox.warning(self, 'Внимание', 'Введено некорректное значение')
 #          QMessageBox.information(self, 'Информация', 'Введено валидное число: "{}"'.format(value))
    
    def update(self):
        cur = self.conn.cursor()
        if self.val_id_house != self.id_house or self.val_num_entr != self.num_entr:
            sql_query = """UPDATE public.entrance
                           SET id_house=%s, num_entr=%s                                                                                             
                           WHERE id_entr=%s"""
            cur.execute(sql_query, (self.val_id_house, self.val_num_entr, self.id_entr))               
            self.conn.commit()
        if self.val_ip_rassbery!=self.ip_rassbery or self.val_port_rassbery!=self.port_rassbery or self.val_login_user!=self.login_user or self.val_pwd_user!=self.pwd_user or self.val_fdb_login!=self.fdb_login or self.val_fdb_password!=self.fdb_password or self.val_fdb_path!=self.fdb_path or self.val_version_fdb!=self.version_fdb:
            sql_query = """UPDATE save.login_data
                           SET ip_rassbery=%s, port_rassbery=%s, login_user=%s, pwd_user=%s, 
                                fdb_login=%s, fdb_password=%s, fdb_path=%s, version_fdb=%s                                                                                             
                           WHERE id_entr=%s"""
            cur.execute(sql_query, (self.val_ip_rassbery, self.val_port_rassbery, self.val_login_user, self.val_pwd_user, self.val_fdb_login, self.val_fdb_password, self.val_fdb_path, self.val_version_fdb, self.id_entr))               
            self.conn.commit()
        cur.close()
        
    def insert(self):
        cur = self.conn.cursor()
        sql_query = """INSERT INTO public.entrance(id_house, num_entr)                                                                                             
                       VALUES (%s, %s) RETURNING id_entr;"""
        cur.execute(sql_query, (self.val_id_house, self.val_num_entr))                
        self.conn.commit()
        data = cur.fetchall()
        self.id_entr = data[0][0]
        sql_query = """INSERT INTO save.login_data(id_entr, ip_rassbery, port_rassbery, login_user, pwd_user, fdb_login, fdb_password, fdb_path, version_fdb)                                                                                             
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        cur.execute(sql_query, (self.id_entr, self.val_ip_rassbery, self.val_port_rassbery, self.val_login_user, self.val_pwd_user, self.val_fdb_login, self.val_fdb_password, self.val_fdb_path, self.val_version_fdb))                
        #self.conn.commit()
        cur.close()
       
    def open_kpu(self):
        self.kpu = kpu.Kpu(self.conn, self.id_entr)
        self.close()
    
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
        self.list_id_street = [0]
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
        for index,row in enumerate(data):   
            self.list_id_street.append(data[index][1])
            self.comboBox_street.addItem(str(data[index][0]))    
        cur.close() 
        
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
        