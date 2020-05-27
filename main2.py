#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import psycopg2
import fdb
import traceback
import configparser
import menu_ui, scaut, kpu, pu, connected_BD_ui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
from PyQt5.Qt import *

# def create_connection(db_name, db_user, db_password, db_host, db_port):
        # connection = None
        # try:
            # connection = psycopg2.connect(
                # database=db_name,
                # user=db_user,
                # password=db_password,
                # host=db_host,
                # port=db_port,
            # )
            # print("Connection to the PostgreSQL DB successful.\nname = ",db_name,"\nuser = ",db_user,"\npassword = ",db_password,"\nhost = ",db_host,"\nport = ",db_port)
        # # except OperationalError as e:
            # # print(f"The error '{e}' occurred")
        # except:
            # msg = QMessageBox()
            # msg.setWindowTitle("Ошибка")
            # msg.setText("Не удалось подключиться к базе данных:") 
            # msg.setInformativeText("name = "+db_name+"\nuser = "+db_user+"\npassword = "+db_password+"\nhost = "+db_host+"\nport = "+db_port)
            # msg.exec()
        # return connection    

class Connection_BD(QtWidgets.QWidget, connected_BD_ui.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.center()  
        self.setWindowTitle('Подключение к базе данных PostgreSQL')
        self.pushButton_continue.clicked.connect(self.open_menu)
        self.show() 
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def open_menu(self):
        try:
            self.conn = self.create_connection()
            self.menu = Menu(self.conn)
        except: print (traceback.format_exc())
    
     
    def create_connection(self):
        connection = None
        try:
            db_name = self.lineEdit_database.text()
            db_user = self.lineEdit_user.text()
            db_password = self.lineEdit_password.text()
            db_host = self.lineEdit_host.text()
            db_port = self.lineEdit_port.text()
            connection = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
            print("Connection to the PostgreSQL DB successful.\nname = ",db_name,"\nuser = ",db_user,"\npassword = ",db_password,"\nhost = ",db_host,"\nport = ",db_port)
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Не удалось подключиться к базе данных:") 
            msg.setInformativeText("name = "+db_name+"\nuser = "+db_user+"\npassword = "+db_password+"\nhost = "+db_host+"\nport = "+db_port)
            msg.exec()
        return connection  
        
class Menu(QtWidgets.QMainWindow, menu_ui.Ui_MainWindow):
    def __init__(self, conn):
        super().__init__()
        self.setupUi(self)
        self.center()        
        self.setWindowTitle('Главное меню')
        self.action_scaut.triggered.connect(self.open_scaut)
        self.action_kpu.triggered.connect(self.open_kpu)
        self.action_pu.triggered.connect(self.open_pu)
        self.action_quit.triggered.connect(self.close)
        self.action_lineState.triggered.connect(self.select_line_state)
        self.tableWidget_replaceKPU.show()
        self.tableWidget_replacePU.show()
        self.label_replaceKPU.show()
        self.label_replacePU.show()
        self.tableWidget_lineState.hide()
        self.label_lineState.hide()
        self.select_kpu(conn)
        self.select_pu(conn)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
                    
    def open_scaut(self,conn):
        self.scaut = scaut.Scaut(conn)

    def open_kpu(self,conn):
        self.kpu = kpu.Kpu(conn,'-1')

    def open_pu(self,conn):
        self.pu = pu.Pu(conn,'-1')

    def select_kpu(self,conn):
        self.tableWidget_replaceKPU.setRowCount(0)       
        sql_query = """ SELECT  old.ser_num, new.ser_num, kpu_replace.date_replace
                            FROM
                             cnt.kpu_replace  
                             inner join cnt.kpu old
                             on old.id_kpu = kpu_replace.id_old_kpu
                             inner join cnt.kpu new
                             on new.id_kpu = kpu_replace.id_new_kpu"""
        cur = conn.cursor()
        cur.execute(sql_query)   
        data = cur.fetchall()
        for index,row in enumerate(data):
            self.tableWidget_replaceKPU.insertRow(0)
            for k in range(len(row)):
                    item = QTableWidgetItem('' if data[index][k]==None else str(data[index][k]))                 
                    self.tableWidget_replaceKPU.setItem(0,k,item)               
        cur.close()    
        self.tableWidget_replaceKPU.resizeColumnsToContents()
        
    def select_pu(self,conn):
        self.tableWidget_replacePU.setRowCount(0)       
        sql_query = """ SELECT  old.serial_number, new.serial_number, counter_replace.date_replace
                            FROM
                             cnt.counter_replace  
                             inner join cnt.counter as old
                             on old.id_klemma = counter_replace.id_old_counter
                             inner join cnt.counter as new
                             on new.id_klemma = counter_replace.id_new_counter"""
        cur = conn.cursor()
        cur.execute(sql_query)   
        data = cur.fetchall()
        for index,row in enumerate(data):
            self.tableWidget_replacePU.insertRow(0)
            for k in range(len(row)):
                    item = QTableWidgetItem('' if data[index][k]==None else str(data[index][k]))                 
                    self.tableWidget_replacePU.setItem(0,k,item)               
        cur.close()    
        self.tableWidget_replacePU.resizeColumnsToContents()

    def select_line_state(self,conn):
        self.tableWidget_replaceKPU.hide()
        self.tableWidget_replacePU.hide()
        self.label_replaceKPU.hide()
        self.label_replacePU.hide()
        self.tableWidget_lineState.show()
        self.label_lineState.show()
        self.tableWidget_lineState.setRowCount(0)       
        sql_query = """ SELECT  
                          city.city_name, street.street_name,
                          house.house_number,
                          entrance.num_entr,		 	
                          flat.flatfloor,		 	
                          flat.num_flat,		 	
                          kpu.ser_num,
                          counter.klemma,				
                          counter.serial_number,
                            case counter.type_counter 		 	
                            when 1 then 'ГВС'
                            when 2 then 'ХВС'
                            when 3 then 'Т'
                            when 4 then 'Э' 
                          end AS Тип,
                          marka.name_marka,
                          date_value.value_zn,
                          date_value.impulse_value,	
                          date_value.line_state,	
                          date_value.empty,  	 
                          counter.last_date
                          
                        FROM
                          cnt.counter
                          left join public.flat
                            on flat.id_flat = counter.id_flat
                          left join cnt.date_value
                            on counter.id_klemma = date_value.id_klemma
                          left join cnt.kpu 
                            on kpu.id_kpu = counter.id_kpu
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

                          WHERE 
                            date_value.date_val = counter.last_date
                            and (date_value.line_state = 1								
                            or date_value.empty = 1)								
                            and working_capacity = 'TRUE'
                          order by city.city_name DESC, street.street_name DESC, cast(substring(house.house_number from \'^[0-9]+\') as integer) DESC, cast(entrance.num_entr as integer) DESC, flat.num_flat DESC, date_value.date_val DESC, counter.type_counter DESC"""
        cur = conn.cursor()
        cur.execute(sql_query)   
        data = cur.fetchall()
        for index,row in enumerate(data):
            self.tableWidget_lineState.insertRow(0)
            for k in range(len(row)):
                    item = QTableWidgetItem('' if data[index][k]==None else str(data[index][k]))                 
                    self.tableWidget_lineState.setItem(0,k,item)               
        cur.close()    
        self.tableWidget_lineState.resizeColumnsToContents()
            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #conn = create_connection("counters", "counters", "counters", "192.168.105.30", "5432")
    #ex = Menu()
    ex = Connection_BD()
    sys.exit(app.exec_())
    conn.close()
    
