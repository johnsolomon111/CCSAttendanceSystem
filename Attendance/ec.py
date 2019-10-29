from PyQt5 import QtWidgets,QtCore
import sys
import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from db_connection import export_data, search_request, fetch_items, fetch_items1, add_request, update_budget, fetch_budget, delete_request, insert_request



class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window,self).__init__()
        centwid=QtWidgets.QWidget()

        self.mylineEdit = QtWidgets.QLineEdit()
        self.mylineEdit2 = QtWidgets.QLineEdit()
        self.mylineEdit3 = QtWidgets.QLineEdit()
        self.mylineEdit4 = QtWidgets.QLineEdit()
        self.mylineEdit5 = QtWidgets.QLineEdit()
        self.startNew=1
        #initialise to empty string on start up
        self.mylineEdit.setText(' ')



        #barcode scans here and then a returnPressed is registered

        self.mylineEdit.hide()


        self.mylineEdit3.hide()
        self.mylineEdit4.hide()
        self.mylineEdit5.hide()


        total, items = fetch_items()
        print(str(total))

        message = QtWidgets.QLabel(centwid)
        message.setText("Options")

        # Create widget
        self.label = QtWidgets.QLabel(self)
        pixmap = QPixmap('logo.jpg')
        self.label.setPixmap(pixmap)

        self.title = QtWidgets.QLabel(centwid)
        self.title.setText("Student Adding")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.hide()

        self.additem = QtWidgets.QLabel(centwid)
        self.additem.setText("RFID Number")
        self.additem.hide()

        self.entername = QtWidgets.QLabel(centwid)
        self.entername.setText("Enter Name")
        self.entername.hide()


        self.enterprice = QtWidgets.QLabel(centwid)
        self.enterprice.setText("ID Number")
        self.enterprice.hide()

        self.enterquantity = QtWidgets.QLabel(centwid)
        self.enterquantity.setText("Pre-enrollment Attendance?(Enter 1 if None)")
        self.enterquantity.hide()


        self.insert_item = QtWidgets.QLabel(centwid)
        self.insert_item.setText(" ")


        total, items = fetch_items()



        item_name = []
        prices_ = []
        item_values = []
        item_barcode = []

        items1 = fetch_items1()
        for item in items1:
           item_name.append(str(item[0]))
           prices_.append(str(item[1]))
           item_values.append(str(item[2]))
           item_barcode.append(str(item[2]))

        print(item_name)
        print(prices_)

        self.tableWidget = QTableWidget()
        # set row count
        self.tableWidget.setObjectName("tableStudents")
        self.tableWidget.setRowCount(len(items1))
        # set column count
        self.tableWidget.setColumnCount(4)

        self.tableWidget.setHorizontalHeaderLabels(['Name', 'Attendance Count', 'ID', 'RFID'])

        pc = int(len(item_name)) -1
        i = 0
        while i <= pc:
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(item_name[i]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(prices_[i]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(item_values[i]))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(item_barcode[i]))
            i += 1

        self.tableWidget.hide()

        self.b3 = QtWidgets.QPushButton('Add Student')
        self.b3.setSizePolicy(
        QtWidgets.QSizePolicy.Preferred,
        QtWidgets.QSizePolicy.Expanding)
        self.b3.clicked.connect(self.btn_click1)


        self.b4 = QtWidgets.QPushButton('Studentbase')
        self.b4.clicked.connect(self.btn_click2)
        self.b4.setSizePolicy(
        QtWidgets.QSizePolicy.Preferred,
        QtWidgets.QSizePolicy.Expanding)

        self.b5 = QtWidgets.QPushButton('Export Data')
        self.b5.clicked.connect(self.btn_click3)
        self.b5.setSizePolicy(
        QtWidgets.QSizePolicy.Preferred,
        QtWidgets.QSizePolicy.Expanding)


        self.submititem = QtWidgets.QPushButton('Submit')
        self.submititem.clicked.connect(self.btn_submititem)
        self.submititem.hide()


        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(message)
        v_box.addWidget(self.b3)
        v_box.addWidget(self.b4)
        v_box.addWidget(self.b5)

        v_box.addStretch()
        v_box.addStretch()
        v_box.addStretch()

        curr_budget = fetch_budget()
        curr_budget = curr_budget[0]


        








        v_box1 =QtWidgets.QVBoxLayout()
        v_box1.addWidget(self.title)
        v_box1.addWidget(self.label)

        v_box1.addWidget(self.additem)
        v_box1.addWidget(self.mylineEdit)
        v_box1.addWidget(self.entername)
        v_box1.addWidget(self.mylineEdit5)
        v_box1.addWidget(self.enterprice)
        v_box1.addWidget(self.mylineEdit3)
        v_box1.addWidget(self.enterquantity)
        v_box1.addWidget(self.mylineEdit4)

        
        v_box1.addWidget(self.submititem)
        v_box1.addWidget(self.insert_item)
        v_box1.addWidget(self.tableWidget)
        v_box1.addStretch()



        lay=QtWidgets.QHBoxLayout()



        
        lay.addLayout(v_box1)
        lay.addLayout(v_box)

        centwid.setLayout(lay)

        
        self.setCentralWidget(centwid)
        self.show()

    def btn_click(self):
        sender = self.sender()
        if sender.text() == 'Enter Budget':
            print(self.le.text())
            budget = float(self.le.text())
            update_budget(budget)
            curr_budget = fetch_budget()
            curr_budget = curr_budget[0]
            self.budget_status.setText("Budget: " + str(curr_budget))
            self.restart_program()

    def btn_click1(self):
        self.title.show()
        self.mylineEdit.show()
        self.additem.show()
        self.enterprice.show()
        self.enterquantity.show()
        self.mylineEdit3.show()
        self.mylineEdit4.show()
        self.mylineEdit5.show()
        self.entername.show()
        self.submititem.show()
        self.tableWidget.hide()

    def btn_click2(self):
        item_name = []
        prices_ = []
        item_values = []
        item_barcode = []

        items1 = fetch_items1()
        for item in items1:
           item_name.append(str(item[0]))
           prices_.append(str(item[1]))
           item_values.append(str(item[2]))
           item_barcode.append(str(item[3]))
           

        # set column count
        self.tableWidget.setColumnCount(4)

        pc = int(len(item_name)) -1
        i = 0
        while i <= pc:
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(item_name[i]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(prices_[i]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(item_values[i]))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(item_barcode[i]))
            i += 1

        self.tableWidget.show()
        self.title.setText("Student Enrollment")
        self.title.show()
        self.mylineEdit.hide()
        self.additem.hide()
        self.enterprice.hide()
        self.enterquantity.hide()
        self.mylineEdit3.hide()
        self.mylineEdit4.hide()
        self.mylineEdit5.hide()
        self.entername.hide()
        self.submititem.hide()


    def btn_click3(self):
        csv_export = export_data()
        self.title.setText(csv_export)
        self.title.show()



        #self.restart_program()
    def btn_submititem(self):
        self.item =self.mylineEdit.text()
        self.price =self.mylineEdit3.text()
        self.quantity =self.mylineEdit4.text()
        self.name =self.mylineEdit5.text()
        if self.price != '':
            request = insert_request(str(self.item).strip(), str(self.name), str(self.quantity), self.price)
        else:
            request = insert_request(str(self.item).strip(), str(self.name), str(self.quantity), 1)

        if request is True:
            self.insert_item.setText("Successfully Enrolled Student")
        else:
            self.insert_item.setText(str(request))


        #set the sample name variable
    def set_sample_name(self):
        self.sample_name = self.mylineEdit.text()
        print(self.sample_name)
        item, value = search_request(self.sample_name)
        print(str(item) + '-' + str(value))
        add_request(str(item), str(value))
        self.update()
        self.startNew=1


    def delete_previous(self,text):
        if self.startNew:
            self.mylineEdit.setText(text[-1])
            self.startNew=0

    def restart_program(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, * sys.argv)



app=QtWidgets.QApplication(sys.argv)

ex=window()
ex.setWindowTitle('EC Attendance - Admin')
ex.setGeometry(100, 100, 800, 480)
sys.exit(app.exec_())