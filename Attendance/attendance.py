from PyQt5 import QtWidgets,QtCore
import sys
import os
import sip
from db_connection import clear_scan, search_request, fetch_items, add_request, update_budget, fetch_budget, delete_request, search_request_delete, reduce_quantity_scan, reduce_quantity_item, increase_quantity_item, search_request_delete_item
from PyQt5.QtGui import QIcon, QPixmap
import datetime

class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window,self).__init__()
        centwid=QtWidgets.QWidget()

        self.mylineEdit = QtWidgets.QLineEdit()

        f = self.mylineEdit.font()
        f.setPointSize(24) # sets the size to 27
        self.mylineEdit.setFont(f)


        self.mylineEdit2 = QtWidgets.QLineEdit()


        self.startNew=1
        #initialise to empty string on start up
        self.mylineEdit.setText(' ')
        self.toggle = False

        #barcode scans here and then a returnPressed is registered

        #connect to a function
        self.mylineEdit.returnPressed.connect(self.set_sample_name) #here is where I want to delete the previous entry without backspacing by hand
        self.mylineEdit.textChanged.connect(self.delete_previous)


        total, items = fetch_items()
        print(str(total))
        self.v_box = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel(centwid)
        f = message.font()
        f.setPointSize(7) # sets the size to 27
        f.setBold(True)
        message.setFont(f)

        self.v_box.addWidget(message)



        self.v_box.addStretch()
        self.v_box.addStretch()
        self.v_box.addStretch()

        curr_budget = fetch_budget()
        curr_budget = curr_budget[0]

        self.welcome = QtWidgets.QLabel(centwid)
        self.welcome.setText("CCS ATTENDANCE")
        f = self.welcome.font()
        f.setPointSize(24) # sets the size to 27
        f.setBold(True)
        self.welcome.setFont(f)




        self.le = QtWidgets.QLineEdit()
        g = self.le.font()
        g.setPointSize(24) # sets the size to 27
        self.le.setFont(g)

        self.budget = QtWidgets.QPushButton('Create/Update Event')
        self.budget.setSizePolicy(
        QtWidgets.QSizePolicy.Preferred,
        QtWidgets.QSizePolicy.Expanding)


        self.done = QtWidgets.QPushButton('Exit')
        self.done.setSizePolicy(
        QtWidgets.QSizePolicy.Preferred,
        QtWidgets.QSizePolicy.Expanding)


        self.budget_status = QtWidgets.QLabel(centwid)
        self.budget_status.setText("EVENT: ")
        f = self.budget_status.font()
        f.setPointSize(10) # sets the size to 27
        f.setBold(True)
        self.budget_status.setFont(f)

        self.message1 = QtWidgets.QLabel(centwid)
        self.message1.setText("ID NUMBER: ")
        f = self.message1.font()
        f.setPointSize(10) # sets the size to 27
        f.setBold(True)
        self.message1.setFont(f)


        self.message2 = QtWidgets.QLabel(centwid)
        self.message2.setText("STUDENT NAME: ")
        f = self.message2.font()
        f.setPointSize(10) # sets the size to 27
        f.setBold(True)
        self.message2.setFont(f)

        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        self.message3 = QtWidgets.QLabel(centwid)
        self.message3.setText(" ")

        self.message4 = QtWidgets.QLabel(centwid)
        self.message4.setText("DATE: " + str(self.date))
        f = self.message4.font()
        f.setPointSize(10) # sets the size to 27
        f.setBold(True)
        self.message4.setFont(f)

        self.budget_message = QtWidgets.QLabel(centwid)


        # self.budget_message.setText("Budget Status: " + str(status))
        f = self.budget_message.font()
        f.setPointSize(10) # sets the size to 27
        f.setBold(True)
        self.budget_message.setFont(f)

        self.v_box1 =QtWidgets.QVBoxLayout()


        # Create widget
        self.label = QtWidgets.QLabel(self)
        pixmap = QPixmap('logo.jpg')
        self.label.setPixmap(pixmap)


        self.v_box1.addWidget(self.welcome)
        self.v_box1.addWidget(self.label)
        self.v_box1.addWidget(self.le)
        self.v_box1.addWidget(self.budget)
        # # self.v_box1.addWidget(self.budget_message)
        self.v_box1.addWidget(self.message4)
        self.v_box1.addWidget(self.budget_status)
        self.v_box1.addWidget(self.message1)
        self.v_box1.addWidget(self.message2)
        self.v_box1.addWidget(self.mylineEdit)
        self.v_box1.addWidget(self.message3)
        self.v_box1.addWidget(self.done)
        self.v_box1.addStretch()
        self.v_box1.addStretch()



        lay=QtWidgets.QHBoxLayout()



        
        lay.addLayout(self.v_box1)
        lay.addLayout(self.v_box)
 


        centwid.setLayout(lay)
        self.budget.clicked.connect(self.btn_click)
        self.done.clicked.connect(self.btn_click3)
        
        self.setCentralWidget(centwid)

        self.show()

    def btn_click(self):
      
        sender = self.sender()

        if self.le.text() != '':

            if sender.text() == 'Create/Update Event':
                if self.toggle is True:
                    print(self.le.text())
                    budget = self.le.text()
                    self.budget_status.setText("EVENT: " + str(budget))
                    self.le.hide()
                    self.toggle = False
                else:
                    self.toggle = True
                    self.le.show()
        else:
        	self.budget_status.setText("No Event Input")


    def btn_click1(self):
        sender = self.sender()
        item = sender.text()
        item = item.split('-')[0]
        item = item.strip()
        item, quantity = search_request_delete(item)
        if item is False: 
        	delete_request(item)
        	self.restart_program()
        else:
            print(str(quantity))
            if int(quantity) == 1:
               delete_request(item)
            else:
               reduce_quantity_scan(item)
               increase_quantity_item(item)
            self.restart_program()

    def btn_click3(self):
         QtWidgets.QMessageBox.about(self, "","Attendance Taking Finished!")
         app.quit()

        #set the sample name variable
    def set_sample_name(self):
        self.sample_name = self.mylineEdit.text()
        print(self.sample_name)
        request = search_request(self.sample_name)
        if request is not False:
            item, value = search_request(self.sample_name)
            if value == '':
                value = ''


            budget = self.le.text()
            print(str(item) + '-' + str(value))
            added = add_request(str(item), str(value), str(budget), str(self.date))
            if added:
                increase_quantity_item(str(item))
                self.restart_program()
                self.startNew=1
                self.message1.setText("ID NUMBER: " + str(value))
                self.message2.setText("STUDENT NAME: " + str(item))
                self.message3.setText("Attendance Taken")
            else:
                self.restart_program()
                self.startNew
                self.message1.setText("ID NUMBER: " + str(value))
                self.message2.setText("STUDENT NAME: " + str(item))
                self.message3.setText("Attendance taken for this event!")               
        else:
            self.message3.setText("Student does not exist")
            self.startNew=1

    def delete_previous(self,text):
        if self.startNew:
            self.mylineEdit.setText(text[-1])
            self.startNew=0


    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def restart_program(self):

    
            total, items = fetch_items()
            print(items)

            self.clearLayout(self.v_box)
                     


            item, value = search_request(self.sample_name)

            self.message2.setText("STUDENT NAME: " + str(item))
            f = self.message2.font()
            f.setPointSize(10) # sets the size to 27
            f.setBold(True)
            self.message2.setFont(f)




   

app=QtWidgets.QApplication(sys.argv)

ex=window()
ex.setWindowTitle('EC Attendance')
ex.setGeometry(100, 100, 800, 480)
sys.exit(app.exec_())
