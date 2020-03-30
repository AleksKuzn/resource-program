import sys
import psycopg2
import scaut_ui, add_scaut_ui, kpu
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QTableWidgetItem
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Scaut(QtWidgets.QWidget, scaut_ui.Ui_Form):
    def __init__(self, conn):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('СКАУТ')      
        self.conn = conn
        
#        self.pushButton_add.hide()
        
        self.pushButton_add.clicked.connect(self.add_window)
        self.tableWidget_scaut.doubleClicked.connect(self.cell_was_clicked)        
        self.scaut_query()
        self.filtr_city()
        self.pushButton_filtr.clicked.connect(self.scaut_query)
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
        
    def scaut_query(self):
        self.tableWidget_scaut.setRowCount(0)
        cur = self.conn.cursor()
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
        cur.execute(self.sql_query)        
        data = cur.fetchall()
        for index,row in enumerate(data):
            self.tableWidget_scaut.insertRow(0)
            for k in range(len(row)):
                item = QTableWidgetItem(str(data[index][k]))
                self.tableWidget_scaut.setItem(0,k,item)        
        cur.close()
        self.tableWidget_scaut.setMouseTracking(True)
        self.current_hover2 = 0
        self.tableWidget_scaut.cellEntered.connect(self.line_selection)
        
    def line_selection(self, row, column):
        if self.current_hover2 != row:
            for j in range(self.tableWidget_scaut.columnCount()):
                self.tableWidget_scaut.item(self.current_hover2, j).setBackground(QBrush(QColor('white')))
                self.tableWidget_scaut.item(row, j).setBackground(QBrush(QColor('lightGray')))
        self.current_hover2 = row
        
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
        self.conn = conn 
        self.filtr_city()
        cur = self.conn.cursor()            
        if id_scaut=='-1':
            self.setWindowTitle('Добавить СКАУТ')
            self.pushButton_kpu.hide()
            self.pushButton_save.clicked.connect(self.insert)
        if id_scaut!='-1':      
            self.setWindowTitle('информация СКАУТ')
            self.pushButton_kpu.show()
            self.pushButton_kpu.clicked.connect(self.open_kpu)
            self.pushButton_save.clicked.connect(self.update)
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
#            self.filtr_city(data[0][0])
#            self.filtr_street(data[0][1])
#            self.filtr_house(data[0][2])
#            self.lineEdit_street.setText(data[0][1])
#            self.lineEdit_house.setText(data[0][2])
            self.lineEdit_entrance.setText(str(data[0][3]))
            self.lineEdit_login.setText(data[0][4])
            self.lineEdit_pasw.setText(data[0][5])
            self.lineEdit_host.setText(data[0][6])
            self.lineEdit_port.setText(str(data[0][7]))
            self.id_entr = data[0][8]
            self.label.setText('id_entr = '+str(data[0][8]))
        cur.close() 
        self.show()

    def update(self):
        #Как проверить, что пользователь не удалил запись из ячейки?
        cur = self.conn.cursor() 
        
        # sql_query = "UPDATE public.entrance SET login_user='" + str(self.lineEdit_login.text()) + "' WHERE id_entr=" + str(self.id_entr) 
        # print(sql_query)               
        # cur.execute(sql_query) 
        sql_query = """UPDATE public.entrance
                       SET login_user=%s                                                                                             
                       WHERE id_entr=%s""" 
        cur.execute(sql_query, (self.lineEdit_login.text(), self.id_entr))        
        
        # sql_query = """INSERT INTO public.entrance(ip_rassbery, port_rassbery, login_user, pwd_user)                                                                                             
                       # VALUES (%s, %s, %s, %s)"""
        # cur.execute(sql_query, (self.lineEdit_host, self.lineEdit_port, self.lineEdit_login, self.lineEdit_pasw))        
        
#        self.conn.commit()
        cur.close()
        
        # sql_query = """INSERT INTO public.entrance(
                                    # id_house, num_entr, ip_rassbery, 
                                    # port_rassbery, login_user, pwd_user)                                                                                             
                            # VALUES ((SELECT id_house 
                                     # FROM public.house 
                                     # WHERE house.house_number = %s), 
                                     # %s, %s, %s, %s, %s);"""
            # cur.execute(sql_query, (self.lineEdit_house, self.lineEdit_entrance, self.lineEdit_host, self.lineEdit_port, self.lineEdit_login, self.lineEdit_pasw))        
            # conn.commit()
            # cur.close()
            
        # INSERT INTO public.entrance(
            # id_house, num_entr, ip_rassbery, port_rassbery)
            # VALUES (
            # (SELECT id_house
          # FROM public.house
          # WHERE house_number = '9' and id_street = (SELECT id_street FROM public.street WHERE street_name = 'Поленова')),
            # 2,3,4);
            
        # self.lineEdit_city
        # self.lineEdit_street
        # self.lineEdit_house
        # self.lineEdit_entrance
        # self.lineEdit_login
        # self.lineEdit_pasw
        # self.lineEdit_host
        # self.lineEdit_port
        
        self.close()
        
    def insert(self):
        cur = self.conn.cursor()
        sql_query = """INSERT INTO public.entrance(ip_rassbery, port_rassbery, login_user, pwd_user)                                                                                             
                        VALUES (%s, %s, %s, %s)"""
        cur.execute(sql_query, (self.lineEdit_host, self.lineEdit_port, self.lineEdit_login, self.lineEdit_pasw))        
#        self.conn.commit()
        cur.close()        
        self.close()
        
    def open_kpu(self):
        self.kpu = kpu.Kpu(self.conn, self.id_entr)
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
#        self.comboBox_city.setCurrentText(city)
#        self.filtr_street()
#        self.comboBox_city.currentIndexChanged.connect(self.filtr_street)      
        
    def filtr_street(self,street):     
        self.comboBox_street.clear()        
        self.comboBox_street.id = []        
        self.comboBox_street.addItem('')
        print(self.comboBox_city.currentIndex())
        
        cur = self.conn.cursor() 
        street_query = """SELECT
                            street.street_name,	
                            street.id_street                             
                        FROM
                            public.street"""                     
        street_query = street_query + " WHERE street.id_city = " + str(self.list_id_city[self.comboBox_city.currentIndex()]) + " order by street.street_name"                      
        cur.execute(street_query)        
        data = cur.fetchall()
        self.list_id_street = []
        for index,row in enumerate(data):   
            self.list_id_street.append(data[index][1])
            self.comboBox_street.addItem(str(data[index][0]))    
        cur.close()      
        self.comboBox_street.setCurrentText(street)
        print(self.comboBox_street.currentIndex())
#        self.filtr_house('9')
        self.comboBox_street.currentIndexChanged.connect(self.filtr_house)
        
    def filtr_house(self,name_house):    
        n_house=name_house
        print(self.comboBox_city.currentIndex())
        print(self.comboBox_street.currentIndex())
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
        print('0')
        cur.execute(house_query)         
        data = cur.fetchall()
        self.list_id_house = []
        for index,row in enumerate(data):  
            self.list_id_house.append(data[index][1])  
            self.comboBox_house.addItem(str(data[index][0]))  
        cur.close()
        self.comboBox_street.setCurrentText(house)
        