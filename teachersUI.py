from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from _sqlite3 import Error
import sys


class TeachersView(object):
    def setupUi(self, Teachers):
        Teachers.setWindowTitle('Teachers')

        Teachers.setObjectName("Teachers")
        Teachers.resize(800, 650)

        self.centralwidget = QtWidgets.QWidget(Teachers)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 70, 771, 391))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.error = QtWidgets.QLabel(self.centralwidget)
        self.error.setEnabled(False)
        self.error.setGeometry(QtCore.QRect(10, 580, 771, 16))
        self.error.setText("")
        self.error.setObjectName("error")

        self.name = QtWidgets.QLineEdit(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(45, 500, 161, 20))
        self.name.setObjectName("name")

        self.refresh = QtWidgets.QPushButton(self.centralwidget)
        self.refresh.setGeometry(QtCore.QRect(697, 45, 85, 24))
        self.refresh.setText('Обновить')
        self.refresh.clicked.connect(self.update_results)

        self.delete = QtWidgets.QPushButton(self.centralwidget)
        self.delete.setGeometry(QtCore.QRect(530, 45, 150, 24))
        self.delete.setText('Удалить учителей')
        self.delete.clicked.connect(self.delete_elem)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 50, 150, 16))
        self.label.setObjectName("label")
        self.label.setText("Учителя")

        self.teacher_label = QtWidgets.QLabel(self.centralwidget)
        self.teacher_label.setGeometry(QtCore.QRect(20, 480, 200, 16))
        self.teacher_label.setObjectName("teacher_label")
        self.teacher_label.setText("Добавить учителя:")

        self.subject_label = QtWidgets.QLabel(self.centralwidget)
        self.subject_label.setGeometry(QtCore.QRect(20, 530, 250, 16))
        self.subject_label.setObjectName("subject_label")
        self.subject_label.setText("Добавить предмет учителю:")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 500, 41, 16))
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Имя:")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(250, 550, 200, 20))
        self.label_4.setObjectName("label_4")
        self.label_4.setText("Предмет:")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 550, 80, 16))
        self.label_5.setObjectName("label_5")
        self.label_5.setText("Учитель:")

        self.subject_ids = {i: j for j, i in enumerate([i[0] for i in self.sqlite_db.request("SELECT title FROM subjects")])}
        self.teachers_ids = {i: j for j, i in self.sqlite_db.request("SELECT id, name FROM teachers")}

        self.teacher_selector = QtWidgets.QComboBox(self.centralwidget)
        self.teacher_selector.setGeometry(QtCore.QRect(75, 550, 161, 20))
        self.teacher_selector.setObjectName("teacher_selector")
        self.teacher_selector.addItems(self.teachers_ids.keys())

        self.subject_selector = QtWidgets.QComboBox(self.centralwidget)
        self.subject_selector.setGeometry(QtCore.QRect(320, 550, 161, 20))
        self.subject_selector.setObjectName("teacher_selector")
        self.subject_selector.addItems(self.subject_ids.keys())

        self.add_teacher = QtWidgets.QToolButton(self.centralwidget)
        self.add_teacher.setGeometry(QtCore.QRect(220, 500, 21, 21))
        self.add_teacher.setObjectName("add_teacher")
        self.add_teacher.setText("+")
        self.add_teacher.clicked.connect(self.add_teacher_to_db)

        self.add_subject = QtWidgets.QToolButton(self.centralwidget)
        self.add_subject.setGeometry(QtCore.QRect(500, 550, 21, 21))
        self.add_subject.setObjectName("add_subject_to_teacher")
        self.add_subject.setText("+")
        self.add_subject.clicked.connect(self.add_subject_to_teacher)

        Teachers.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Teachers)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        Teachers.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Teachers)
        self.statusbar.setObjectName("statusbar")
        Teachers.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(Teachers)

        self.update_results()

    def update_results(self):
        cur = self.sqlite_db.get_cur()

        res = cur.execute("""SELECT teachers.id, name, title FROM teachers LEFT JOIN subjects_to_teachers ON
         teachers.id = teacher_key LEFT JOIN subjects ON subjects.id = subject_key""").fetchall()

        self.tableWidget.setRowCount(len(res))

        if not res:
            self.error.setText('Ничего не найдено')
            return
        else:
            self.error.setText('')

        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Имя', 'Предмет'])

        for i, element in enumerate(res):
            for j, val in enumerate(element):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))

    def add_teacher_to_db(self):
        name = self.name.text()
        if name == '':
            self.error.setText("Неправильно введены данные")
            return

        try:
            self.sqlite_db.request(f"INSERT INTO teachers (name) VALUES('{self.name.text()}')")
            self.sqlite_db.commit()
        except Error:
            self.error.setText("Не удалось добавить учителя")

        self.update_results()
        self.update_selectors()
        self.error.setText('')

    def add_subject_to_teacher(self):
        teacher_id = self.teachers_ids.get(self.teacher_selector.currentText())
        subject_id = self.subject_selector.currentIndex()

        try:
            self.sqlite_db.request(f"INSERT INTO subjects_to_teachers VALUES({teacher_id}, {subject_id})")
            self.sqlite_db.commit()
        except Error:
            self.error.setText("Не удалось добавить учителя")

        self.update_results()
        self.update_selectors()
        self.error.setText('')

    def update_selectors(self):
        self.subject_ids = {i: j for j, i in enumerate([i[0] for i in self.sqlite_db.request("SELECT title FROM subjects")])}
        self.teachers_ids = {i: j for j, i in self.sqlite_db.request("SELECT id, name FROM teachers")}

        self.teacher_selector.addItems(self.teachers_ids.keys())
        self.subject_selector.addItems(self.subject_ids.keys())

    def delete_elem(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]

        if not ids:
            self.error.setText('Учителя не выбраны')
            return

        valid = QMessageBox.question(
            self, '', f"Действительно удалить учителей с id {', '.join(ids)}?",
            QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            self.sqlite_db.request('DELETE FROM teachers WHERE id IN ("{}")'.format('", "'.join(ids)))
            self.sqlite_db.request('DELETE FROM subjects_to_teachers WHERE teacher_key IN ("{}")'.format('", "'.join(ids)))
            self.sqlite_db.commit()

        self.error.setText('')
        self.update_results()


class TeachersWindowWidget(QMainWindow, TeachersView):
    def __init__(self, sqlite_db):
        super().__init__()
        self.sqlite_db = sqlite_db
        self.setupUi(self)