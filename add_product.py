import operator

import mysql.connector
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtPrintSupport, QtGui, uic,QtWidgets
import sys
from PyQt5.uic import loadUi


class Ui_Add_Product(QtWidgets.QDialog):
    def setupProductUi(self, Dialog):
        Dialog.setObjectName('salim')
        loadUi("add_product_form.ui", Dialog)
    





    




if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    uiProduct = Ui_Add_Product()
    uiProduct.setupProductUi(uiProduct)
    uiProduct.show()
    sys.exit(app.exec_())