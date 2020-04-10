import sys
import psycopg2
import datetime
import KPU_ui, add_KPU_ui, replace_KPU_ui, pu   
from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtWidgets import  QTableWidgetItem, QCheckBox
#from PyQt5.QtGui import *
from PyQt5.Qt import *
from datetime import timedelta 
       
class Kpu(QtWidgets.QWidget, KPU_ui.Ui_Form):
    def __init__(self, conn, id_entr):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('КПУ')
        self.id_entr=id_entr
        self.conn = conn 
        self.pushButton_add.clicked.connect(self.add_window)
        self.tableWidget_kpu.doubleClicked.connect(self.cell_was_clicked)        
        self.select()
        self.pushButton_filtr.clicked.connect(self.select)
        self.tableWidget_kpu.horizontalHeader().hideSection(0)
        self.tableWidget_kpu.horizontalHeader().hideSection(10)
        self.filtr_city()
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
        if (self.id_entr!='-1') and (self.tableWidget_kpu.rowCount() > 0):
            self.comboBox_city.setCurrentText(self.tableWidget_kpu.item(0,1).text())
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
        if (self.id_entr!='-1') and (self.tableWidget_kpu.rowCount() > 0):
            self.comboBox_street.setCurrentText(self.tableWidget_kpu.item(0,2).text())
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
        if (self.id_entr!='-1') and (self.tableWidget_kpu.rowCount() > 0):
            self.comboBox_house.setCurrentText(self.tableWidget_kpu.item(0,3).text())
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
        if (self.id_entr!='-1') and (self.tableWidget_kpu.rowCount() > 0):
            self.comboBox_entrance.setCurrentText(self.tableWidget_kpu.item(0,4).text())
            self.id_entr='-1'
    
    def select(self):
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
                              left join public.entrance
                                on entrance.id_entr = kpu.id_entr
                              left join public.house
                                on house.id_house = entrance.id_house
                              left join public.street
                                on street.id_street = house.id_street
                              left join public.city
                                on city.id_city = street.id_city"""
        if self.id_entr!='-1':
            self.sql_query = self.sql_query + " WHERE kpu.id_entr = " + str(self.id_entr)
            self.tableWidget_kpu.horizontalHeader().hideSection(1)
        if self.id_entr=='-1':
            if self.comboBox_city.currentText()!='':
                self.tableWidget_kpu.horizontalHeader().hideSection(1)
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
            else: self.tableWidget_kpu.horizontalHeader().showSection(1)
        self.sql_query = self.sql_query + " ORDER BY city.city_name, street.street_name, cast(substring(house.house_number from \'^[0-9]+\') as integer), cast(entrance.num_entr as integer), kpu.type_kpu, kpu.adress DESC"     
        cur = self.conn.cursor()
        cur.execute(self.sql_query)   
        data = cur.fetchall()
        for index,row in enumerate(data):
            self.tableWidget_kpu.insertRow(0)
            for k in range(len(row)):
#                if str(data[index][k])!='':
#                    item = QTableWidgetItem(str(data[index][k]))
                    item = QTableWidgetItem('' if data[index][k]==None else str(data[index][k]))                 
                    self.tableWidget_kpu.setItem(0,k,item)
                    if data[index][10]==0:
                        self.tableWidget_kpu.item(0, k).setBackground(QtGui.QColor(245,245,245))
                        self.tableWidget_kpu.item(0, k).setForeground(QtGui.QColor(110,110,110))                   
        cur.close()    
        self.tableWidget_kpu.resizeColumnsToContents()
#        self.tableWidget_kpu.resizeRowsToContents()
        self.tableWidget_kpu.setMouseTracking(True)
        self.current_hover = 0
        self.tableWidget_kpu.cellEntered.connect(self.line_selection)
    
    def line_selection(self, row, column):
        if self.current_hover != row:
            for j in range(self.tableWidget_kpu.columnCount()):
                if self.tableWidget_kpu.item(self.current_hover,10).text()=='0':        
                    self.tableWidget_kpu.item(self.current_hover, j).setBackground(QtGui.QColor(245,245,245))                   
                else:
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
        self.widget_kpuNew.hide()
        self.label_error.hide()
        self.resize(500,300)
        self.id_kpu = id_kpu 
        self.conn = conn 
        self.filtr_city() 
        self.filtr_type()
        self.lineEdit_serial.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.lineEdit_floor.setValidator(QRegExpValidator(QRegExp("[0-9][0-9]")))
        self.pushButton_save.clicked.connect(self.verify) 
        if self.id_kpu=='-1':
            self.setWindowTitle('Добавить КПУ')
            self.tabWidget_kpu.setTabEnabled(1,False)
            self.tabWidget_kpu.setTabText(1,'')
            self.pushButton_pu.hide()
            self.pushButton_replace.hide()
            self.comboBox_city.setCurrentText('Обнинск')
            self.comboBox_street.setCurrentText('Поленова')
            
        if self.id_kpu!='-1':      
            self.setWindowTitle('Изменить информацию о КПУ')
            self.pushButton_pu.show()    
            self.pushButton_replace.show()
            self.pushButton_pu.clicked.connect(self.open_pu)
            self.pushButton_replace.clicked.connect(self.show_replace)
            self.select_history()
            cur = self.conn.cursor()
            self.sql_query = """SELECT
                              city.city_name, street.street_name,
                              house.house_number, entrance.num_entr,
                              kpu.ser_num, kpu.adress,
                              kpu.type_kpu, kpu.floor,
                              kpu.note, kpu.workability, kpu.id_entr	                            
                            FROM
                              cnt.kpu
                              left join public.entrance
                                on entrance.id_entr = kpu.id_entr
                              left join public.house
                                on house.id_house = entrance.id_house
                              left join public.street
                                on street.id_street = house.id_street
                              left join public.city
                                on city.id_city = street.id_city
                            WHERE kpu.id_kpu = %s"""
            cur.execute(self.sql_query, (self.id_kpu, ))
            data = cur.fetchall()
            self.city_name = data[0][0]
            self.street_name = data[0][1]
            self.house_number = data[0][2]
            self.num_entr = data[0][3]
            self.ser_num = data[0][4]
            self.adress = data[0][5]
            self.type_kpu = data[0][6]
            self.floor = data[0][7]
            self.note = data[0][8]
            self.workability = data[0][9]
            self.id_entr = data[0][10]
            self.comboBox_city.setCurrentText(self.city_name)
            self.comboBox_city.model().item(0).setEnabled(False)
            self.comboBox_street.setCurrentText(self.street_name)
            self.comboBox_street.model().item(0).setEnabled(False)
            self.comboBox_house.setCurrentText(self.house_number)
            self.comboBox_house.model().item(0).setEnabled(False)
            self.comboBox_entrance.setCurrentText(str(self.num_entr))
            self.comboBox_entrance.model().item(0).setEnabled(False)
            self.lineEdit_floor.setText('' if self.floor==None else str(self.floor))
            self.lineEdit_serial.setText('' if self.ser_num==None else str(self.ser_num))
            self.spinBox_adress.setValue(self.adress)
            self.comboBox_type.setCurrentText(str(self.type_kpu))
            self.textEdit_note.setText(self.note)
            self.checkBox.setChecked(self.workability)
            self.label.setText('id_kpu = ' + self.id_kpu)
            cur.close()
        self.show()
    
    def select_history(self):
        self.tableWidget_history.setRowCount(0)       
        self.sql_query = """SELECT city.city_name, street.street_name,
                                   house.house_number, entrance.num_entr,
                                   kpu_history.floor, kpu_history.adress,  
                                   kpu_history.workability, 
                                   kpu_history.date_change, kpu_history.note                           
                            FROM
                              cnt.kpu
                              inner join cnt.kpu_history
                                on kpu_history.id_kpu = kpu.id_kpu
                              left join public.entrance
                                on entrance.id_entr = kpu.id_entr
                              left join public.house
                                on house.id_house = entrance.id_house
                              left join public.street
                                on street.id_street = house.id_street
                              left join public.city
                                on city.id_city = street.id_city
                            WHERE kpu.id_kpu = %s
                            ORDER BY city.city_name, street.street_name, cast(substring(house.house_number from \'^[0-9]+\') as integer), cast(entrance.num_entr as integer) DESC"""       
        cur = self.conn.cursor()
        cur.execute(self.sql_query, (self.id_kpu,))   
        data = cur.fetchall()
        for index,row in enumerate(data):
            self.tableWidget_history.insertRow(0)
            for k in range(len(row)):
                    item = QTableWidgetItem('' if data[index][k]==None else str(data[index][k]))                 
                    self.tableWidget_history.setItem(0,k,item)                 
        cur.close()    
        self.tableWidget_history.resizeColumnsToContents()
    
    def verify(self): #Доработать ошибки
        try:
            text='Введено некорректное значение'   
            if self.comboBox_entrance.currentText()=='': 
                text='Введите номер подъезда'
                raise ValueError
            self.val_adress = int(self.spinBox_adress.value())
            self.val_id_entr = int(self.list_id_entrace[self.comboBox_entrance.currentIndex()])
            self.val_type = int(self.comboBox_type.currentText())
            self.val_serial = str(self.lineEdit_serial.text())
            self.val_serial = None if self.val_serial == '' else int(self.val_serial)
            self.val_floor = str(self.lineEdit_floor.text())
            self.val_floor = None if self.val_floor == '' else int(self.val_floor)
            self.val_note = str(self.textEdit_note.text())
            if self.val_note == '': self.val_note = None
            self.val_work = int(self.checkBox.isChecked())
            if self.id_kpu=='-1':
                self.insert()
            if self.id_kpu!='-1':
                self.update()
        except ValueError:         
                pal = self.label_error.palette()
                pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
                self.label_error.setPalette(pal)
                #self.resize(self.label_error.sizeHint())    
                self.label_error.setText(text)        
                self.label_error.show()     
    
    def update(self):
        cur = self.conn.cursor()
        sql_query = """ UPDATE cnt.kpu
                        SET adress=%s, id_entr=%s, type_kpu=%s, ser_num=%s, floor=%s, note=%s, workability=%s 
                        WHERE id_kpu=%s"""
        cur.execute(sql_query, (self.val_adress, self.val_id_entr, self.val_type, self.val_serial, self.val_floor, self.val_note, self.val_work, self.id_kpu))               
        #self.conn.commit()
        cur.close()
        self.close()

    def insert(self):
        cur = self.conn.cursor()
        sql_query = """INSERT INTO cnt.kpu(adress, id_entr, type_kpu, ser_num, 
                                            floor, note, workability)                                                                                             
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cur.execute(sql_query, (self.val_adress, self.val_id_entr, self.val_type, self.val_serial, self.val_floor, self.val_note, self.val_work))                
        #self.conn.commit()
        cur.close()                
        self.close()
   
    def open_pu(self):
        self.pu = pu.Pu(self.conn, self.id_kpu)
        self.close()
    
    def show_replace(self):
        #self.center()
        self.resize(900,300)
        self.widget_kpuNew.show()
        self.setWindowTitle('Замена КПУ')
        self.label_errorNew.hide()
        self.pushButton_selectDate.hide()
        self.flag_selectDate=True
        self.comboBox_city.setCurrentText(self.city_name)
        self.comboBox_street.setCurrentText(self.street_name)
        self.comboBox_house.setCurrentText(self.house_number)
        self.comboBox_entrance.setCurrentText(str(self.num_entr))
        self.lineEdit_floor.setText('' if self.floor==None else str(self.floor))
        self.lineEdit_serial.setText('' if self.ser_num==None else str(self.ser_num))
        self.spinBox_adress.setValue(self.adress)
        self.comboBox_type.setCurrentText(str(self.type_kpu))
        self.textEdit_note.setText(self.note)
        self.checkBox.setChecked(self.workability)
        self.tabWidget_kpu.setEnabled(False)
        self.lineEdit_serialNew.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        self.comboBox_typeNew.setCurrentText(str(self.type_kpu))
        #self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        #self.dateTimeEdit.setDisplayFormat("dd.MM.yyyy hh:mm")
        if int(datetime.datetime.today().strftime('%M'))<30:
            date_st = datetime.datetime.today() - timedelta(hours=1)
        else: date_st = datetime.datetime.today()
        self.dateTimeEdit.setDateTime(date_st.replace(minute=0, second=0))
        self.processing_klemma()
        self.checkBox.setChecked(False)
        self.checkBoxNew.setChecked(True)
        self.widget_st_zn.show() if self.checkBox_st_zn.isChecked() else self.widget_st_zn.hide()
        self.checkBox_st_zn.stateChanged.connect(self.change_box)
        self.pushButton_canselNew.clicked.connect(self.cansel)
        self.pushButton_replaceNew.clicked.connect(self.replace_kpu)
        self.pushButton_selectDate.clicked.connect(self.select_date)
        self.comboBox_typeNew.currentIndexChanged.connect(self.change_type)
    
    def change_type(self):
        #self.doubleSpinBox_k8.setDecimals(3)
        if self.comboBox_typeNew.currentText() == '3':
            x=13
            while x<=16: 
                exec('self.lineEdit_k%s.show()' % x)
                exec('self.label_k%s.show()' % x)
                x+=1
        else:
            x=13
            while x<=16: 
                exec('self.lineEdit_k%s.hide()' % x)
                exec('self.label_k%s.hide()' % x)
                exec('self.lineEdit_k%s.setEnabled(False)' % x)
                x+=1
    
    def processing_klemma(self):
        self.change_type()
        x=1
        while x<=16: 
            exec('self.lineEdit_k%s.setEnabled(False)' % x)
            exec('self.lineEdit_k%s.setValidator(QRegExpValidator(QRegExp("[0-9]{1,5}[\\.]{1,1}[0-9]{1,4}")))' % x)
            #exec('self.doubleSpinBox_k%s.setEnabled(False)' % (x))
            x+=1

    def change_box(self):
        if self.checkBox_st_zn.isChecked(): 
            self.widget_st_zn.show()
            self.pushButton_selectDate.show()
        else: 
            self.widget_st_zn.hide()   
            self.pushButton_selectDate.hide()
     
    def cansel(self):    
        self.resize(500,300)
        self.widget_kpuNew.hide()
        self.setWindowTitle('Изменить информацию о КПУ')
        self.tabWidget_kpu.setEnabled(True)
        self.checkBox.setChecked(self.workability)
    
    def replace_kpu(self):
        try:
            text='Введено некорректное значение'
            if self.flag_selectDate and self.checkBox_st_zn.isChecked():
                text='Выберите дату и нажмите обновить'
                raise ValueError
            if self.lineEdit_serialNew.text()=='': 
                text='Введите серийный номер'
                raise ValueError
            self.val_typeNew = int(self.comboBox_typeNew.currentText())
            self.val_serialNew = int(self.lineEdit_serialNew.text())
            self.val_noteNew = str(self.lineEdit_noteNew.text())
            if self.val_noteNew == '': self.val_noteNew = None
            self.val_workNew = int(self.checkBoxNew.isChecked())
            self.date_val = self.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm:00")
            cur = self.conn.cursor()
            sql_query = """ UPDATE cnt.kpu
                            SET id_entr=%s, workability=%s 
                            WHERE id_kpu=%s"""
            cur.execute(sql_query, (6, 0, self.id_kpu))          
            #self.conn.commit()
            cur.close()
            cur = self.conn.cursor()
            sql_query = """ SELECT kpu.id_kpu, counter.id_klemma
                            FROM cnt.kpu 
                            left join cnt.counter
                                on counter.id_kpu=kpu.id_kpu
                            WHERE kpu.ser_num = %s"""
            cur.execute(sql_query, (self.val_serialNew,))       
            data = cur.fetchall()
            cur.close()
            if len(data)==1:
                self.id_kpuNew=data[0][0]
                cur = self.conn.cursor()
                sql_query = """ UPDATE cnt.kpu
                                SET id_entr=%s, workability=%s 
                                WHERE id_kpu=%s"""
                cur.execute(sql_query, (self.id_entr, self.val_workNew, self.id_kpuNew))          
                #self.conn.commit()
                cur.close()
                if self.checkBox_st_zn.isChecked():
                    self.start_value()                 
            if len(data)==0:
                cur = self.conn.cursor()
                sql_query = """INSERT INTO cnt.kpu(adress, id_entr, type_kpu, ser_num, 
                                                    floor, note, workability)                                                                                             
                            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cur.execute(sql_query, (self.adress, self.id_entr, self.val_typeNew, self.val_serialNew, self.floor, self.val_noteNew, self.val_workNew))                
                #self.conn.commit()
                cur.close()
                if self.checkBox_st_zn.isChecked():
                    self.start_value()                    
            if len(data)>1:
                text='КПУ имеет подключенные ПУ'
                raise ValueError
            cur = self.conn.cursor()
            sql_query = """INSERT INTO cnt.kpu_replace(id_old_kpu, id_new_kpu, date_replace)                                                                                             
                           VALUES (%s,(SELECT kpu.id_kpu FROM cnt.kpu WHERE kpu.ser_num=%s),%s)"""
            cur.execute(sql_query, (self.id_kpu, self.val_serialNew, self.date_val))                
            #self.conn.commit()
            cur.close()           
            self.close()
        except ValueError:
                pal = self.label_errorNew.palette()
                pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
                self.label_errorNew.setPalette(pal)  
                self.label_errorNew.setText(text)        
                self.label_errorNew.show()     
        
    def start_value(self):
        cur = self.conn.cursor()
        for index,row in enumerate(self.data_pu):
            num_klemma=self.data_pu[index][1]
            exec('self.st_value=self.lineEdit_k%s.text()' % num_klemma)
            sql_query = """INSERT INTO cnt.start_value(id_klemma,date_val,st_value,impulse_value)
                           VALUES (%s,%s,%s,0)"""
            cur.execute(sql_query, (self.data_pu[index][4], self.date_val, float(self.st_value)))                 
            #self.conn.commit()
        cur.close()
                   
    def select_date(self):
        self.flag_selectDate=False
        date_val = self.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:00:00")
        print(date_val)
        self.sql_query = """SELECT date_value.value_zn, counter.klemma, flat.num_flat,
                                case counter.type_counter
                                    when 1 then 'ГВС'
                                    when 2 then 'ХВС'
                                    when 3 then 'Т'
                                    when 4 then 'Э' 
                                end AS type, counter.id_klemma
                            FROM cnt.counter
                              inner join cnt.date_value
                                on date_value.id_klemma = counter.id_klemma
                              inner join public.flat
                                on flat.id_flat = counter.id_flat
                            WHERE counter.id_kpu = %s and date_value.date_val = %s"""
        cur = self.conn.cursor()                
        cur.execute(self.sql_query, (self.id_kpu, date_val))
        self.data_pu = cur.fetchall()
        for index,row in enumerate(self.data_pu):
            exec('self.lineEdit_k%s.setEnabled(True)' % self.data_pu[index][1])
            exec('self.label_k%s.setText("№%s %s")' % (self.data_pu[index][1], self.data_pu[index][2], self.data_pu[index][3]))
            exec('self.lineEdit_k%s.setText("%s")' % (self.data_pu[index][1], self.data_pu[index][0]))

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
    
    def filtr_type(self):
        self.comboBox_type.clear()
        self.comboBox_typeNew.clear()
    #    self.comboBox_type.id = []        
    #    self.comboBox_type.addItem('')
        cur = self.conn.cursor()
        entrance_query = """SELECT	
                            DISTINCT kpu.type_kpu                             
                        FROM
                            cnt.kpu""" 
        cur.execute(entrance_query) 
        data = cur.fetchall()
        for index,row in enumerate(data):        
            self.comboBox_type.addItem(str(data[index][0]))
            self.comboBox_typeNew.addItem(str(data[index][0]))
        cur.close()