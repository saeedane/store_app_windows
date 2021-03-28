import operator
from datetime import date
import MySQLdb
import pandas as pandas
import qrcode
from PyQt5 import QtPrintSupport, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import sys
import db_structure
from PyQt5.uic import loadUi
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog

ui, _ = uic.loadUiType('mainwindow.ui')

# Calculator state.
from PyQt5.uic import loadUi, loadUiType

READY = 0
INPUT = 1


class MainWindow(QMainWindow, ui):
    def db_connect(self):
        self.db = MySQLdb.connect(user='root', password='',
                                  host='localhost', database='store_app', charset='utf8')
        self.cur = self.db.cursor()

        print('connect database')

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        loadUi("mainwindow.ui", self)
        self.db_connect()
        self.setupApp()
        self.home()
        self.handelButton()
        self.calculator()
        self.showSuppliers()
        self.showProductStoke()
        self.showProductSale()
        self.showInvoiceSale()
        self.showUserData()

    def setupApp(self):
        self.tabWidget.tabBar().hide()

    def handelButton(self):
        self.pushButton_2.clicked.connect(self.home)
        self.pushButton_3.clicked.connect(self.product)
        self.pushButton_4.clicked.connect(self.sales)
        self.pushButton_5.clicked.connect(self.stoke)
        self.pushButton_6.clicked.connect(self.raport)
        self.pushButton_7.clicked.connect(self.factor)
        self.pushButton_8.clicked.connect(self.setting)
        self.pushButton.clicked.connect(self.checkLogin)
        self.pushButton_54.clicked.connect(self.addProduct)
        self.pushButton_19.clicked.connect(self.searchProduct)
        self.pushButton_46.clicked.connect(self.addSuppliers)
        self.pushButton_48.clicked.connect(self.openFile)
        self.pushButton_55.clicked.connect(self.filterProduct)
        self.pushButton_53.clicked.connect(self.updateProduct)
        self.pushButton_52.clicked.connect(self.deleteProduct)
        # button handle stock page
        self.pushButton_19.clicked.connect(self.addStock)
        # button handle sale product  page
        self.pushButton_20.clicked.connect(self.addProductSale)

        # button handle sale product invoice
        self.pushButton_59.clicked.connect(self.addInvoiceSale)

        # button handle rest price
        self.pushButton_13.clicked.connect(self.restPrice)
        self.pushButton_14.clicked.connect(self.restCalculate)

        # button add permission add username
        self.pushButton_51.clicked.connect(self.userPermission)
        self.pushButton_43.clicked.connect(self.addUser)

    # set index tab for button

    def home(self):
        self.tabWidget.setCurrentIndex(0)

    def sales(self):
        self.tabWidget.setCurrentIndex(1)

    def product(self):
        self.tabWidget.setCurrentIndex(2)

    def stoke(self):
        self.tabWidget.setCurrentIndex(3)

    def raport(self):
        self.tabWidget.setCurrentIndex(4)

    def factor(self):
        self.tabWidget.setCurrentIndex(5)

    def setting(self):
        self.tabWidget.setCurrentIndex(6)

    def checkLogin(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if username == 'salim' and password == "123":
            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.groupBox.setEnabled(True)
            self.groupBox_4.setEnabled(True)
            self.groupBox_10.setEnabled(True)
            self.groupBox_3.setEnabled(True)
            self.groupBox_6.setEnabled(True)
            self.groupBox_12.setEnabled(True)

    def addUser(self):
        name = self.lineEdit_36.text()
        password = self.lineEdit_38.text()
        confirm_pass = self.lineEdit_39.text()

        self.cur.execute(
            ''' insert into users (name, password, confirm_pass) values(%s,%s,%s)''',
            (name, password, confirm_pass))
        self.db.commit()

        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setText("تم اضافة مستخدم   بنجاح ")
        message.exec_()

    def userPermission(self):
        username = self.comboBox.currentText()
        tab_home = 0
        tab_product = 0
        tab_stock = 0
        tab_product_sale = 0
        tab_setting = 0
        tab_permission = 0
        tab_show_Invoice = 0
        tab_report = 0

        if username != 'اسم المستخدم ':

            if self.checkBox_32.isChecked():
                tab_product = 1
            if self.checkBox_30.isChecked():
                tab_product_sale = 1
            if self.checkBox_29.isChecked():
                tab_stock = 1
            if self.checkBox_27.isChecked():
                tab_report = 1
            if self.checkBox_36.isChecked():
                tab_show_Invoice = 1
            if self.checkBox_28.isChecked():
                tab_setting = 1
            if self.checkBox_35.isChecked():
                tab_home = 1
            if self.checkBox_31.isChecked():
                tab_product = 1
                tab_product_sale = 1
                tab_stock = 1
                tab_report = 1
                tab_show_Invoice = 1
                tab_setting = 1
                tab_home = 1
            self.cur.execute(''' SELECT name FROM users  where name=%s''', [(username)])
            user = self.cur.fetchall()
            for data in user:
                print(data[0])
                if data[0] == username:

                    self.cur.execute(''' SELECT user FROM userpermission ''')
                    permission = self.cur.fetchall()
                    for perm in permission:
                        if perm[0] == username:
                            message = QMessageBox()
                            message.setIcon(QMessageBox.Warning)
                            message.setText(" اسم موجد في قاعدة البيانت  ")
                            message.exec_()
                        else:
                            self.cur.execute(
                                ''' insert into userpermission (user ,tab_home, tab_product, tab_product_sale, tab_stock, tab_setting, tab_permission, tab_show_Invoice, tab_report) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                (
                                    username, tab_home, tab_product, tab_product_sale, tab_stock, tab_setting,
                                    tab_permission,
                                    tab_show_Invoice,
                                    tab_report))
                            self.db.commit()
                            self.checkBox_32.setChecked(False)
                            self.checkBox_29.setChecked(False)
                            self.checkBox_27.setChecked(False)
                            self.checkBox_36.setChecked(False)
                            self.checkBox_28.setChecked(False)
                            self.checkBox_35.setChecked(False)
                            self.checkBox_31.setChecked(False)
                            message = QMessageBox()
                            message.setIcon(QMessageBox.Information)
                            message.setText("تم اضافة صلاحيات  بنجاح ")
                            message.exec_()

    def showUserData(self):
        self.comboBox.clear
        self.cur.execute(''' SELECT name FROM users''')
        user = self.cur.fetchall()
        for query in user:
            self.comboBox.addItem(query[0])

    def openFile(self):

        filePath = QFileDialog.getOpenFileName(self, 'a file', '*.jpg')
        self.lineEdit_6.setText(filePath[0])
        pixmap = QPixmap(filePath[0])
        self.label_37.setPixmap(pixmap)

    def showProductStoke(self):
        self.tableWidget_2.setRowCount(0)
        self.cur.execute(''' SELECT  * FROM stock''')

        data = self.cur.fetchall()
        if data:
            for row, item in enumerate(data):
                self.tableWidget_2.insertRow(row)
                for col, items in enumerate(item):
                    if col == 9:
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(items)))
                        if item[9] == item[8]:
                            self.stoke()
                            message = QMessageBox()
                            message.setIcon(QMessageBox.Warning)
                            message.setText(" بقيت من كمية منتج " + item[1] + "5")
                            message.exec_()
                    else:
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(items)))
                        col += 1
                rowPosition = self.tableWidget_2.rowCount()
                self.tableWidget_2.removeRow(rowPosition)

    def showProductSale(self):

        self.tableWidget_4.setRowCount(0)
        self.cur.execute(''' SELECT  * FROM productsale''')

        data = self.cur.fetchall()
        if data:
            for row, item in enumerate(data):
                self.tableWidget_4.insertRow(row)
                for col, items in enumerate(item):
                    self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(items)))
                    col += 1
                rowPosition = self.tableWidget_4.rowCount()
                self.tableWidget_4.removeRow(rowPosition)

    def showInvoiceSale(self):
        self.tableWidget_5.setRowCount(0)
        self.cur.execute(''' SELECT  product_name, quantity, product_sum FROM productsale''')
        data = self.cur.fetchall()
        if data:
            for row, item in enumerate(data):
                self.tableWidget_5.insertRow(row)
                for col, items in enumerate(item):
                    self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(items)))
                    col += 1
                rowPosition = self.tableWidget_5.rowCount()
                self.tableWidget_5.removeRow(rowPosition)
        self.sumPrice()
        sumCal = self.lcdNumber_2.value()

        self.label_22.setText('  اجمالي  :  ' + str(sumCal) + 'دج')

        self.addProductSale()

    def addInvoiceSale(self):
        code = self.lineEdit_50.text()

        datetime = QDateTime.currentDateTime()

        Invoice_date = datetime.toString()
        product_sale = [self.tableWidget_5.item(row, 2).text() for row in range(self.tableWidget_5.rowCount())]
        product_name = [self.tableWidget_5.item(row, 0).text() for row in range(self.tableWidget_5.rowCount())]

        quantity = [self.tableWidget_5.item(row, 1).text() for row in range(self.tableWidget_5.rowCount())]
        restPrice = self.label_20.text()
        if self.tableWidget_4.rowCount() >= 1:
            self.pushButton_13.setEnabled(True)
            for i in range(len(product_name)):
                if code == 'رقم فاتورة' and code == '':
                    print("لا تترد حقل فاتورة   فارغ ")
                    message = QMessageBox()
                    message.setIcon(QMessageBox.Warning)
                    message.setText("لا تترد حقل فاتورة فارغ")
                    message.exec_()
                else:
                    data = self.cur.execute('''INSERT INTO invoiceproduct(Invoice_code,Invoice_date,product_sale,product_name,restPrice, quantity, price)VALUES
                                                (%s,%s,%s,%s,%s,%s,%s)''', (
                        [code, Invoice_date, product_sale[i], product_name[i], restPrice, quantity[i], 20]))
                    self.db.commit()
                    if data:
                        message = QMessageBox()
                        message.setIcon(QMessageBox.Information)
                        message.setText("تم اضافة فاتورة بنجاح ")
                        message.exec_()
                        self.showProductSale()



                    else:
                        print('i dont level work ')


    def addProduct(self):
        self.showSuppliers()
        product_name = self.lineEdit_47.text()
        product_code = self.lineEdit_7.text()
        product_suppliers = self.comboBox_10.currentIndex()
        product_date = self.dateTimeEdit_2.date()
        product_image = self.lineEdit_6.text()

        try:

            if product_suppliers == 0:
                print("لا تترد حقل المورد  فارغ ")
                message = QMessageBox()
                message.setIcon(QMessageBox.Warning)
                message.setText("لا تترد حقل المورد فارغ")
                message.exec_()
            else:

                self.cur.execute('''INSERT INTO product(product_name,product_code,product_image,product_date,supplier_id)VALUES
                     (%s,%s,%s,%s,%s)''', (
                    [product_name, product_code, product_image, product_date,
                     product_suppliers]))

                self.db.commit()

                self.lineEdit_47.setText("")
                self.lineEdit_7.setText("")
                self.comboBox_10.setCurrentIndex(0)
                self.lineEdit_7.setText("")
                message = QMessageBox()
                message.setIcon(QMessageBox.Information)
                message.setText("تم اضافة بينات بنجاح ")
                message.exec_()


        except Exception as e:
            print(e)

    def showSuppliers(self):
        self.comboBox_10.clear
        self.cur.execute('''SELECT suppliers_name FROM suppliers ''')
        data = self.cur.fetchall()
        for query in data:
            self.comboBox_10.addItem(query[0])

    def addSuppliers(self):
        supplier_name = self.lineEdit_16.text()
        supplier_id = self.cur.execute(''' SELECT id  FROM suppliers ''')
        parent_id = supplier_id + 1
        if supplier_name == " اسم مورد" or supplier_name == "":
            self.label_35.setText("لا تترك حق فارغ ")
            self.label_35.setStyleSheet("color:red")

        else:
            sql_supp = self.cur.execute('''INSERT INTO suppliers (suppliers_name,parent_id) VALUES (%s,%s)''',
                                        (supplier_name, parent_id))
            if sql_supp != "":
                self.db.commit()
                self.lineEdit_16.setText("")
                self.label_35.setText(" تم اضافة بنجاح ")
                self.label_35.setStyleSheet("color:green")

    def searchProduct(self):
        product_code = self.lineEdit_41.text()

        sql = ''' SELECT * FROM product WHERE product_code = %s '''
        self.cur.execute(sql, [product_code])
        query = self.cur.fetchall()
        print(query)

        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)

        for row, form in enumerate(query):
            for column, item in enumerate(form):
                self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)

    def filterProduct(self):
        product_code = self.lineEdit_35.text()
        sql = (
            ''' select product_name,product_code,product_image,product_date,supplier_id from product WHERE product_code = %s''')
        self.cur.execute(sql, [product_code])

        data = self.cur.fetchall()
        for query in data:
            self.lineEdit_45.setText(str((query[0])))
            self.lineEdit_4.setText(str(query[1]))
            self.lineEdit_3.setText(str(query[2]))
            product_image = self.lineEdit_3.text()

            if product_image != "":
                pixmap = QPixmap(product_image)
                self.label_27.setPixmap(pixmap)
                print(product_image)

            self.lineEdit_19.setText(str(query[3]))
            self.comboBox_6.setCurrentIndex(int(query[4]))

    def updateProduct(self):
        product_name = self.lineEdit_45.text()
        product_code = self.lineEdit_4.text()
        product_suppliers = self.comboBox_6.currentIndex()
        product_date = self.lineEdit_19.text()
        print(product_code)
        product_image = self.lineEdit_3.text()

        try:
            self.cur.execute(
                """ UPDATE product SET product_name = %s,product_image=%s,product_date=%s,supplier_id=%s WHERE product_code=%s """,
                ([product_name, product_image, product_date, product_suppliers, product_code]))
            self.db.commit()

            message = QMessageBox()
            message.setIcon(QMessageBox.Information)
            message.setText("تم تعديل  بينات بنجاح ")
            message.exec_()

        except Exception as e:
            print(e)

    def deleteProduct(self):
        product_code = self.lineEdit_4.text()
        self.cur.execute(''' delete from product WHERE product_code=%s''', ([product_code]))
        self.db.commit()
        self.lineEdit_45.setText("")
        self.lineEdit_4.setText("")
        self.comboBox_6.setCurrentIndex(0)
        self.lineEdit_3.setText("")
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setText("تم حذف  بينات بنجاح ")
        message.exec_()
        print("delete ....")

    def addStock(self):

        product_code = self.lineEdit_43.text()
        sql = (
            ''' select  product_name ,product_code ,supplier_id,product_quantity from product WHERE product_code = %s''')
        self.cur.execute(sql, [product_code])
        data = self.cur.fetchall()

        product_quantity = data[0][3]

        alert_quantity = self.lineEdit_12.text()
        product_sale = self.lineEdit_9.text()
        product_bey = self.lineEdit_10.text()
        product_name = data[0][0]
        product_code = data[0][1]

        product_supplier = data[0][2]

        product_percent = (int(product_bey) - int(product_sale))
        product_sum = (int(product_bey) + int(product_sale))
        self.cur.execute('''INSERT INTO stock(product_name,product_code,product_price,product_sale,product_sum,product_percent,supplier_id,alert_quantity,quantity)VALUES
                               (%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (
            [product_name, product_code, product_bey, product_sale, product_sum, product_percent,
             product_supplier, alert_quantity, product_quantity]))
        self.db.commit()
        self.showProductStoke()
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setText("تم اضافة  بينات بنجاح ")
        message.exec_()
        self.lineEdit_12.setText("")
        self.lineEdit_9.setText("")

    def addProductSale(self):
        try:
            product_code = self.lineEdit_46.text()

            sql = (
                ''' select  product_name  ,product_code , product_sale,quantity from stock WHERE product_code = %s''')
            self.cur.execute(sql, [product_code])
            stock = self.cur.fetchall()
            product_name = stock[0][0]
            code = stock[0][1]
            product_quantity = stock[0][3]
            sale_quantity = self.lineEdit_14.text()
            final_quantity = int(product_quantity) - int(sale_quantity)
            product_sale = stock[0][2]
            product_sum_cal = int(sale_quantity) * int(product_sale)
            self.sumPrice()
            if self.lineEdit_46.text() == '':
                message = QMessageBox()
                message.setIcon(QMessageBox.Warning)
                message.setText(" لا تترك حقل فارغ ")
                message.exec_()
            elif sale_quantity > product_quantity:
                message = QMessageBox()
                message.setIcon(QMessageBox.Warning)
                message.setText(" كمية مطلوبة أكبر من المخزن   ")
                message.exec_()
            else:
                self.cur.execute(
                    """ UPDATE stock SET quantity = %s WHERE product_code=%s """,
                    ([final_quantity, product_code]))
                self.db.commit()
                self.showProductStoke()
                sql = (
                    ''' select  product_code quantity  from productsale WHERE product_code = %s''')
                self.cur.execute(sql, [product_code])
                data = self.cur.fetchall()

                if data:
                    product_code = self.lineEdit_46.text()
                    sale_quantity = self.lineEdit_14.text()
                    sql = (
                        ''' select  quantity , product_sale from stock WHERE product_code = %s''')
                    self.cur.execute(sql, [product_code])

                    stock = self.cur.fetchall()

                    if stock[0][0] == str(0):
                        self.pushButton_20.setEnabled(False)
                        final_quantity = 0
                        sql = (
                            ''' select  quantity from productsale WHERE product_code = %s''')
                        self.cur.execute(sql, [product_code])

                        sale = self.cur.fetchall()
                        update_quantity = int(sale_quantity) + int(sale[0][0])

                        self.cur.execute(
                            """ UPDATE productsale SET quantity = %s WHERE product_code=%s """,
                            ([update_quantity, product_code]))
                        self.db.commit()
                        self.showProductSale()
                        self.cur.execute(
                            """ UPDATE stock SET quantity = %s WHERE product_code=%s """,
                            ([final_quantity, product_code]))
                        self.db.commit()
                        self.showProductStoke()
                        message = QMessageBox()
                        message.setIcon(QMessageBox.Information)
                        message.setText("كمية منتهية لمنتوج " + product_name)
                        message.exec_()
                    elif stock[0][0] > str(0):
                        sql = (
                            ''' select  quantity,product_sum from productsale WHERE product_code = %s''')
                        self.cur.execute(sql, [product_code])

                        sale = self.cur.fetchall()
                        update_quantity = int(sale_quantity) + int(sale[0][0])
                        update_sum = int(update_quantity) * int(stock[0][1])

                        self.cur.execute(
                            """ UPDATE productsale SET quantity = %s ,product_sum=%s WHERE product_code=%s """,
                            ([update_quantity, update_sum, product_code]))
                        self.db.commit()
                        self.showProductSale()

                    else:
                        message = QMessageBox()
                        message.setIcon(QMessageBox.Information)
                        message.setText("كمية مطلوبة غير موجودة  في مخزن  " + product_name)
                        message.exec_()

                else:

                    self.cur.execute('''INSERT INTO productsale(product_code, product_name,product_sum, quantity)VALUES
                                                    (%s,%s,%s,%s)''', (
                        [code, product_name, product_sum_cal, sale_quantity]))

                    self.db.commit()
                    message = QMessageBox()
                    message.setIcon(QMessageBox.Information)
                    message.setText("تم اضافة  بينات بنجاح ")
                    message.exec_()
                    self.lineEdit_14.setText("")
                    self.showProductSale()
                    self.showInvoiceSale()

        except Exception as e:
            print(e)

    def sumPrice(self):
        number = 0
        sumPrice = [self.tableWidget_4.item(row, 3).text() for row in range(self.tableWidget_4.rowCount())]

        for i in range(len(sumPrice)):
            number += int(sumPrice[i])
            self.lcdNumber_2.display(number)

    def restPrice(self):
        try:
            sumCal = self.lcdNumber_2.value()
            price = self.lineEdit_4.text()
            restPrice = int(sumCal) - int(price)

            if price == 'مبلغ مسدد':
                message = QMessageBox()
                message.setIcon(QMessageBox.Warning)
                message.setText('لا تترك حقل تسديد فارغ ')
                message.exec_()
            else:
                message = QMessageBox()
                message.setIcon(QMessageBox.Information)
                message.setText('تم شراء بنجاح  ')
                message.exec_()
                self.printPriviewPdf()
                self.label_22.setText('  اجمالي  :  ' + str(sumCal) + 'دج')
                self.cur.execute(''' delete from productsale''')
                self.pushButton_13.setEnabled(False)

                self.db.commit()
                self.label_22.setText('')
                self.label_20.setText('')
                self.lcdNumber_2.display('0')
                self.tableWidget_5.setRowCount(0)
                self.tableWidget_4.setRowCount(0)




        except Exception as e:
            print(e)

    def restCalculate(self):
        try:

            sumCal = self.lcdNumber_2.value()
            price = self.lineEdit_4.text()
            restPrice = int(sumCal) - int(price)
            self.label_20.setText('  الباقي  :  ' + str(restPrice) + 'دج')
        except Exception as e:
            print(e)

    def printPriviewPdf(self):
        # Create printer
        printer = QtPrintSupport.QPrinter()
        # Create painter
        painter = QtGui.QPainter()
        # Start painter
        painter.begin(printer)
        # Grab a widget you want to print
        screen = self.frame_12.grab()

        print(screen)
        # Draw grabbed pixmap
        painter.drawPixmap(10, 10, screen)
        # End painting
        painter.end()

    def printpreviewDialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.printPreview)
        previewDialog.exec_()

    def printPreview(self, printer):
        self.textEdit.print_(printer)

    def calculator(self):
        # Setup numbers.
        for n in range(0, 10):
            getattr(self, 'pushButton_n%s' % n).pressed.connect(lambda v=n: self.input_number(v))

        # Setup operations.
        self.pushButton_add.pressed.connect(lambda: self.operation(operator.add))
        self.pushButton_sub.pressed.connect(lambda: self.operation(operator.sub))
        self.pushButton_mul.pressed.connect(lambda: self.operation(operator.mul))
        self.pushButton_div.pressed.connect(lambda: self.operation(operator.truediv))  # operator.div for Python2.7

        self.pushButton_pc.pressed.connect(self.operation_pc)
        self.pushButton_eq.pressed.connect(self.equals)

        # Setup actions
        self.actionReset.triggered.connect(self.reset)
        self.pushButton_ac.pressed.connect(self.reset)

        self.actionExit.triggered.connect(self.close)

        self.pushButton_m.pressed.connect(self.memory_store)
        self.pushButton_mr.pressed.connect(self.memory_recall)

        self.memory = 0
        self.reset()

        self.show()

    def display(self):
        self.lcdNumber.display(self.stack[-1])

    def reset(self):
        self.state = READY
        self.stack = [0]
        self.last_operation = None
        self.current_op = None
        self.display()

    def memory_store(self):
        self.memory = self.lcdNumber.value()

    def memory_recall(self):
        self.state = INPUT
        self.stack[-1] = self.memory
        self.display()

    def input_number(self, v):
        if self.state == READY:
            self.state = INPUT
            self.stack[-1] = v
        else:
            self.stack[-1] = self.stack[-1] * 10 + v

        self.display()

    def operation(self, op):
        if self.current_op:  # Complete the current operation
            self.equals()

        self.stack.append(0)
        self.state = INPUT
        self.current_op = op

    def operation_pc(self):
        self.state = INPUT
        self.stack[-1] *= 0.01
        self.display()

    def equals(self):
        # Support to allow '=' to repeat previous operation
        # if no further input has been added.
        if self.state == READY and self.last_operation:
            s, self.current_op = self.last_operation
            self.stack.append(s)

        if self.current_op:
            self.last_operation = self.stack[-1], self.current_op

            try:
                self.stack = [self.current_op(*self.stack)]
            except Exception:
                self.lcdNumber.display('Err')
                self.stack = [0]
            else:
                self.current_op = None
                self.state = READY
                self.display()


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Calculon")

    window = MainWindow()
    app.exec_()
