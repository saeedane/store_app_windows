import operator

import mysql.connector
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtPrintSupport, QtGui, uic,QtWidgets
import sys
from PyQt5.uic import loadUi


class Ui_Dialog(QtWidgets.QDialog):
    def setupUi(self, Dialog):
        loadUi("invoise.ui", Dialog)
          ## coneection between app and DB
        self.db = mysql.connector.connect(host='localhost' ,user='root', password='', db='store_app')
        self.cur = self.db.cursor()
        print('Connection Accepted')
        Dialog.pushButton_13.clicked.connect(self.printer)
        self.frame = Dialog.frame
        self.cur.execute('''SELECT number_invoise,customer,phone FROM invoise ''')
        data = self.cur.fetchall()
        for query in data:
            Dialog.label.setText("اسم المشتري : " + query[1])
            Dialog.label_6.setText("رقم فاتورة  : " + query[0])
            Dialog.label_2.setText("رقم هاتف  : " + query[2])




    def printer(self):
      # Create printer
        printer = QtPrintSupport.QPrinter()
        # Create painter
        painter = QtGui.QPainter()
        # Start painter
        painter.begin(printer)
        # Grab a widget you want to print
        screen = self.frame.grab()

        print(screen)
        # Draw grabbed pixmap
        painter.drawPixmap(10, 10, screen)
        # End painting
        painter.end()
   



    




if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.setupUi(ui)
    ui.show()
    sys.exit(app.exec_())