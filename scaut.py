import sys
import psycopg2
import scaut_ui, add_scaut_ui, kpu
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QTableWidgetItem
from PyQt5.QtGui import *
from PyQt5.Qt import *
#from PyQt5.QtCore import *

class Scaut(QtWidgets.QWidget, scaut_ui.Ui_Form):
    def __init__(self, conn):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('СКАУТ')      
        self.conn = conn
        self.pushButton_add.clicked.connect(self.add_window)
        self.tableWidget_scaut.doubleClicked.connect(self.cell_was_clicked)        
        self.filtr_city()
        self.select()
        self.pushButton_filtr.clicked.connect(self.select)
        self.tableWidget_scaut.horizontalHeader().hideSection(4)
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
        self.sql_query = self.sql_query + " ORDER BY city.city_name, street.street_name, cast(substring(house.house_number from \'^[0-9]+\') as integer), cast(entrance.num_entr as integer) DESC"      
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
        self.add_scaut = add_Scaut('-1', self.conn)

    def cell_was_clicked(self, coords):
        id_scaut=self.tableWidget_scaut.item(coords.row(), 4).text()
        self.add_scaut = add_Scaut(id_scaut, self.conn)    

class add_Scaut(QtWidgets.QWidget, add_scaut_ui.Ui_Form):
    def __init__(self, id_scaut, conn):
        super().__init__()
        self.setupUi(self)
        self.id_scaut = id_scaut 
        self.label_error.hide()
        self.conn = conn 
        self.filtr_city()
        self.lineEdit_port.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.pushButton_save.clicked.connect(self.verify)
        if self.id_scaut=='-1':
            self.setWindowTitle('Добавить СКАУТ')
            self.pushButton_kpu.hide()
            self.comboBox_city.setCurrentText('Обнинск')
            self.comboBox_street.setCurrentText('Поленова')
        if self.id_scaut!='-1':      
            self.setWindowTitle('Изменить СКАУТ')
            self.pushButton_kpu.show()
            self.pushButton_kpu.clicked.connect(self.open_kpu)
            cur = self.conn.cursor()
            self.sql_query = """SELECT
                                    city.city_name,	
                                    street.street_name,
                                    house.house_number,
                                    entrance.num_entr,
                                    entrance.login_user,
                                    entrance.pwd_user,   
                                    entrance.ip_rassbery,
                                    entrance.port_rassbery,
                                    entrance.id_entr                                                                                             
                                FROM
                                    public.entrance
                                left join public.house
                                    on house.id_house = entrance.id_house
                                left join public.street
                                    on street.id_street = house.id_street
                                left join public.city
                                    on city.id_city = street.id_city
                                WHERE entrance.id_entr = %s"""
            cur.execute(self.sql_query, (self.id_scaut, )) 
            data = cur.fetchall()
            self.comboBox_city.setCurrentText(data[0][0])
            self.comboBox_city.model().item(0).setEnabled(False)
            self.comboBox_street.setCurrentText(data[0][1])
            self.comboBox_street.model().item(0).setEnabled(False)
            self.comboBox_house.setCurrentText(data[0][2])
            self.comboBox_house.model().item(0).setEnabled(False) 
            self.spinBox_entr.setValue(data[0][3])
            self.lineEdit_login.setText(data[0][4])
            self.lineEdit_pasw.setText(data[0][5])
            self.lineEdit_host.setText(data[0][6])
            val_port=data[0][7]
            val_port= '' if val_port==None else str(val_port)
            self.lineEdit_port.setText(val_port)
            self.id_entr = data[0][8]
            self.label.setText('id_entr = '+str(data[0][8]))
            cur.close() 
        self.show()
    
    def verify(self):
        try:
           # QMessageBox.information(self, 'Информация', 'Введено валидное число: "{}"'.format(value))
            text='Введено некорректное значение'
            if self.comboBox_house.currentText()=='': 
                text='Введите номер дома'
                raise ValueError
            self.val_id_house = int(self.list_id_house[self.comboBox_house.currentIndex()])
            self.val_entr = int(self.spinBox_entr.value())
            self.val_host = str(self.lineEdit_host.text())
            if self.val_host == '': self.val_host = None
            self.val_port = str(self.lineEdit_port.text())
            self.val_port = None if self.val_port == '' else int(self.val_port)
            self.val_login = str(self.lineEdit_login.text())
            if self.val_login == '': self.val_login = None
            self.val_pasw = str(self.lineEdit_pasw.text())
            if self.val_pasw == '': self.val_pasw = None
            if self.id_scaut=='-1':
                self.insert()
            if self.id_scaut!='-1':
                self.update()
        except ValueError:                         
            pal = self.label_error.palette()
            pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
            self.label_error.setPalette(pal)
            self.label_error.setText(text)     
            self.label_error.show() 
 #           QMessageBox.warning(self, 'Внимание', 'Введено некорректное значение')
    
    def update(self):
        #Как проверить, что пользователь не удалил запись из ячейки?
        cur = self.conn.cursor()
        sql_query = """UPDATE public.entrance
                       SET id_house=%s, num_entr=%s, ip_rassbery=%s, port_rassbery=%s, login_user=%s, pwd_user=%s                                                                                             
                       WHERE id_entr=%s"""
        cur.execute(sql_query, (self.val_id_house, self.val_entr, self.val_host, self.val_port, self.val_login, self.val_pasw, self.id_entr))               
        #self.conn.commit()
        cur.close()
        self.close()
        
    def insert(self):
        cur = self.conn.cursor()
        sql_query = """INSERT INTO public.entrance(id_house, num_entr, ip_rassbery, port_rassbery, login_user, pwd_user)                                                                                             
                       VALUES (%s, %s, %s, %s, %s, %s)"""
        cur.execute(sql_query, (self.val_id_house, self.val_entr, self.val_host, self.val_port, self.val_login, self.val_pasw))                
        #self.conn.commit()
        cur.close()                
        self.close()
       
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
        