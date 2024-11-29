import sys
import os
from PyQt5.QtWidgets import QVBoxLayout,QMessageBox,QTableWidgetItem
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import Qt
import resources


# Main Algorithms
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    while left and right:
        result.append(left.pop(0) if left[0] < right[0] else right.pop(0))
    return result + left + right

def binary_search(arr, target):
    if not arr:
        return []
    
    mid = len(arr) // 2
    if target in arr[mid]:
        return [arr[mid]] + binary_search(arr[:mid], target) + binary_search(arr[mid+1:], target)
    elif target < arr[mid]:
        return binary_search(arr[:mid], target)
    else:
        return binary_search(arr[mid+1:], target)

# Main Window and GUI Functionalities

def showDialog(msg):
	msgBox = QMessageBox()
	msgBox.setIcon(QMessageBox.Information)
	msgBox.setText(msg)
	msgBox.setWindowTitle("Warning")
	msgBox.setStandardButtons(QMessageBox.Ok)
	returnValue = msgBox.exec()

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("GUI.ui", self)
        onlyInt = QtGui.QIntValidator()
        onlyInt.setRange(0,9999999)
        self.ui.lineEdit_2.setValidator(onlyInt)
        self.ui.lineEdit_4.setValidator(onlyInt)
        self.Data = {}
        
        self.ui.add.clicked.connect(self.addStock)
        self.ui.remove.clicked.connect(self.removeStock)
        self.ui.lineEdit_3.textChanged.connect(self.searchMedicines)

    def createCenteredTableWidgetItem(self,text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def addStock(self):
        name = self.ui.lineEdit.text().lower()
        name = name.split(",")
        if name[0] in "      ":
            showDialog("Error: No Name Provided")
            return
        try:
            quantity = int(self.ui.lineEdit_2.text())
        except:
            showDialog('Error: No Quantity Provided')
            return
        try:
            price = float(self.ui.lineEdit_4.text())
        except:
            showDialog('Error: No Price Provided')
            return
        for i in name:
            try:
                test = self.Data[i]
            except:
                self.Data[i] = {'quantity': quantity,'price': price, 'total price': quantity * price}
                self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
                print(self.ui.tableWidget.rowCount())
                self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,0,self.createCenteredTableWidgetItem(i))
                self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,1,self.createCenteredTableWidgetItem(str(quantity)))
                self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,2,self.createCenteredTableWidgetItem(str(price)))
                self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,3,self.createCenteredTableWidgetItem(str(quantity * price)))
                self.sortMedicines()
            else:
                self.Data[i]['quantity'] += quantity
                self.Data[i]['total price'] += quantity * price
                pos = self.ui.tableWidget.row(self.ui.tableWidget.findItems(i,Qt.MatchContains)[0])
                self.ui.tableWidget.setItem(pos,0,self.createCenteredTableWidgetItem(i))
                self.ui.tableWidget.setItem(pos,1,self.createCenteredTableWidgetItem(str(self.Data[i]['quantity'])))
                self.ui.tableWidget.setItem(pos,2,self.createCenteredTableWidgetItem(str(self.Data[i]['price'])))
                self.ui.tableWidget.setItem(pos,3,self.createCenteredTableWidgetItem(str(self.Data[i]['price'] * self.Data[i]['quantity'])))
              
        print(self.Data)

    def sortMedicines(self):
        names = list(self.Data.keys())
        sortedNames = merge_sort(names)
        self.ui.tableWidget.setRowCount(0)
        totalprices = 0

        for i in sortedNames:
            quantity = self.Data[i]['quantity']
            price = self.Data[i]['price']
            totalprices += price*quantity
            self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
            print(self.ui.tableWidget.rowCount())
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,0,self.createCenteredTableWidgetItem(i))
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,1,self.createCenteredTableWidgetItem(str(quantity)))
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,2,self.createCenteredTableWidgetItem(str(price)))
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,3,self.createCenteredTableWidgetItem(str(price * quantity)))
        self.ui.label.setText(f"Total Stock: {totalprices}$")
            
    def searchMedicines(self):
        search = self.ui.lineEdit_3.text()
        if search in "     ":
            self.ui.tableWidget.setRowCount(0)
            self.sortMedicines()
        else:
            self.ui.tableWidget.setRowCount(0)
            names = list(self.Data.keys())
            searched = binary_search(merge_sort(names),search)
            self.readData(merge_sort(searched))

   
    def readData(self,names):
        self.ui.tableWidget.setRowCount(0)
        for i in names:
            quantity = self.Data[i]['quantity']
            price = self.Data[i]['price']
            self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
            print(self.ui.tableWidget.rowCount())
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,0,self.createCenteredTableWidgetItem(i))
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,1,self.createCenteredTableWidgetItem(str(quantity)))
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,2,self.createCenteredTableWidgetItem(str(price)))
            self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount()-1,3,self.createCenteredTableWidgetItem(str(price * quantity)))

    def removeStock(self):
        name = self.ui.lineEdit.text().lower()
        name = name.split(",")
        if name[0] in "      ":
            showDialog("Error: No Name Provided")
            return
        try:
            quantity = int(self.ui.lineEdit_2.text())
        except:
            showDialog('Error: No Quantity Provided')
            return
        for i in name:
            try:
                self.Data[i]
            except:
                pass
            else:
                new_quantity = self.Data[i]['quantity'] - quantity
                new_totalprice = self.Data[i]['total price'] - quantity * self.Data[i]['price']
                if new_quantity <= 0:
                    del self.Data[i]
                else:
                    self.Data[i]['quantity'] = new_quantity
                    self.Data[i]['total price'] = new_totalprice
        self.sortMedicines()