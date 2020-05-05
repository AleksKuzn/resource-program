#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import psycopg2
import menu_ui, scaut, kpu, pu 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
from PyQt5.Qt import *

def create_connection(db_name, db_user, db_password, db_host, db_port):
        connection = None
        try:
            connection = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
            print("Connection to the PostgreSQL DB successful")
        except OperationalError as e:
            print(f"The error '{e}' occurred")
        return connection    
 
class Menu(QtWidgets.QMainWindow, menu_ui.Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()        
        self.setWindowTitle('main')
        self.action_scaut.triggered.connect(self.open_scaut)
        self.action_kpu.triggered.connect(self.open_kpu)
        self.action_pu.triggered.connect(self.open_pu)
        self.action_quit.triggered.connect(self.close)
        self.select_kpu()
        self.select_pu()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
                    
    def open_scaut(self):
        self.scaut = scaut.Scaut(conn)

    def open_kpu(self):
        self.kpu = kpu.Kpu(conn,'-1')

    def open_pu(self):
        self.pu = pu.Pu(conn,'-1')

    def select_kpu(self):
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
        
    def select_pu(self):
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    conn = create_connection("counters", "counters", "counters", "192.168.105.30", "5432")
    ex = Menu()
    sys.exit(app.exec_())
    conn.close()
    
