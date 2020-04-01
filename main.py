import sys
import psycopg2
import menu_ui, scaut, kpu, pu
    
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication

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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    conn = create_connection("counters", "counters", "counters", "192.168.105.30", "5432")
    ex = Menu()
    sys.exit(app.exec_())
    conn.close()
    
