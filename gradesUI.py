from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from _sqlite3 import Error
import sys


class Ui_Teachers(object):
    def setupUi(self, Teachers):
        Teachers.setObjectName("Teachers")
        Teachers.resize(789, 603)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        Teachers.setFont(font)
        self.centralwidget = QtWidgets.QWidget(Teachers)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 50, 771, 431))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.error = QtWidgets.QLabel(self.centralwidget)
        self.error.setEnabled(False)
        self.error.setGeometry(QtCore.QRect(10, 530, 771, 16))
        self.error.setText("")
        self.error.setObjectName("error")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 490, 121, 16))
        self.label_2.setObjectName("label_2")
        self.subj = QtWidgets.QComboBox(self.centralwidget)
        self.subj.setGeometry(QtCore.QRect(50, 510, 141, 22))
        self.subj.setObjectName("subj")
        self.add = QtWidgets.QToolButton(self.centralwidget)
        self.add.setGeometry(QtCore.QRect(200, 510, 21, 21))
        self.add.setObjectName("add")
        self.error_2 = QtWidgets.QLabel(self.centralwidget)
        self.error_2.setEnabled(False)
        self.error_2.setGeometry(QtCore.QRect(10, 540, 771, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.error_2.setFont(font)
        self.error_2.setText("")
        self.error_2.setObjectName("error_2")
        self.subj_4 = QtWidgets.QComboBox(self.centralwidget)
        self.subj_4.setGeometry(QtCore.QRect(60, 10, 181, 22))
        self.subj_4.setObjectName("subj_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 61, 16))
        self.label.setObjectName("label")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 510, 41, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(690, 10, 91, 24))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(540, 510, 75, 24))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(620, 510, 75, 24))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(700, 510, 75, 24))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        Teachers.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Teachers)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 789, 21))
        self.menubar.setObjectName("menubar")
        Teachers.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Teachers)
        self.statusbar.setObjectName("statusbar")
        Teachers.setStatusBar(self.statusbar)

        self.retranslateUi(Teachers)
        QtCore.QMetaObject.connectSlotsByName(Teachers)

    def retranslateUi(self, Teachers):
        _translate = QtCore.QCoreApplication.translate
        Teachers.setWindowTitle(_translate("Teachers", "MainWindow"))
        self.label_2.setText(_translate("Teachers", "Добавить урок:"))
        self.add.setText(_translate("Teachers", "+"))
        self.label.setText(_translate("Teachers", "Класс:"))
        self.label_6.setText(_translate("Teachers", "Урок:"))
        self.pushButton.setText(_translate("Teachers", "Удалить уроки"))
        self.pushButton_2.setText(_translate("Teachers", "Сохранить"))
        self.pushButton_3.setText(_translate("Teachers", "Обновить"))
        self.pushButton_4.setText(_translate("Teachers", "Очистить"))


class GradesWindowWidget(QMainWindow, Ui_Teachers):
    def __init__(self, sqlite_db):
        super().__init__()
        self.sqlite_db = sqlite_db
        self.setupUi(self)