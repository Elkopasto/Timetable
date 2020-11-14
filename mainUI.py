from teachersUI import TeachersWindowWidget
from gradesUI import GradesWindowWidget

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from _sqlite3 import Error
import sys

weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница',
            'Суббота', 'Воскресенье']
grades = [str(i) + ' класс' for i in range(1, 12)]
sqlite_db = None


class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Timetable")
        MainWindow.resize(645, 600)

        self.teachersWindow = None
        self.gradesWindow = None

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.days = QtWidgets.QComboBox(self.centralwidget)
        self.days.setGeometry(QtCore.QRect(10, 10, 191, 21))
        self.days.setObjectName("days")
        self.days.addItems(weekdays)
        self.days.currentIndexChanged.connect(self.update_results)

        self.grades = QtWidgets.QComboBox(self.centralwidget)
        self.grades.setGeometry(QtCore.QRect(210, 10, 220, 21))
        self.grades.setObjectName("grades")
        self.grades.addItems(grades)
        self.grades.currentIndexChanged.connect(self.update_results)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 70, 625, 471))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.teacherEdit = QtWidgets.QToolButton(self.centralwidget)
        self.teacherEdit.setGeometry(QtCore.QRect(560, 10, 76, 21))
        self.teacherEdit.setObjectName("teacherEdit")
        self.teacherEdit.setText("-Учителя-")
        self.teacherEdit.clicked.connect(self.show_teachers_window)

        self.gradeEdit = QtWidgets.QToolButton(self.centralwidget)
        self.gradeEdit.setGeometry(QtCore.QRect(560, 40, 76, 21))
        self.gradeEdit.setObjectName("gradeEdit")
        self.gradeEdit.setText("-Классы-")
        self.gradeEdit.clicked.connect(self.show_grades_window)

        self.error = QtWidgets.QLabel(self.centralwidget)
        self.error.setEnabled(False)
        self.error.setGeometry(QtCore.QRect(10, 540, 771, 16))
        self.error.setText("")
        self.error.setObjectName("error")

        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setGeometry(QtCore.QRect(10, 40, 191, 21))
        self.save.setText("Обновить")

        self.clear = QtWidgets.QPushButton(self.centralwidget)
        self.clear.setGeometry(QtCore.QRect(210, 40, 220, 21))
        self.clear.setText("Стереть все")
        self.clear.clicked.connect(self.delete_all)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

    def update_results(self):
        cur = sqlite_db.get_cur()

        day = self.days.currentIndex()
        grade = self.grades.currentIndex() + 1
        res = cur.execute(f"""SELECT time.time, subjects.title, teachers.name, days.title FROM schedule JOIN time
                                ON time.id = schedule.time JOIN days
                                ON days.id = schedule.day JOIN subjects
                                ON subjects.id = schedule.subj JOIN teachers
                                ON teachers.id = schedule.teacher
                                WHERE schedule.day = {day} AND schedule.grade = {grade}""").fetchall()

        self.tableWidget.setRowCount(len(res))

        if not res:
            self.error.setText('Ничего не найдено')
            return
        else:
            self.error.setText('')

        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setHorizontalHeaderLabels(['Время', 'Предмет', 'Учитель', 'День'])

        for i, element in enumerate(res):
            for j, val in enumerate(element):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))

    def delete_all(self):
        valid = QMessageBox.question(
            self, '', "Вы правда хотите удалить все данные о расписании?",
            QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            try:
                sqlite_db.request("DELETE FROM schedule")
            except Error:
                self.error.setText("Произошла ошиька при удалении данных из БД")
                return

        self.error.setText("")
        self.update_results()

    def show_teachers_window(self):
        if not self.teachersWindow:
            self.teachersWindow = TeachersWindowWidget(sqlite_db)
        self.teachersWindow.show()

    def show_grades_window(self):
        if not self.gradesWindow:
            self.gradesWindow = GradesWindowWidget(sqlite_db)
        self.gradesWindow.show()


class MainWindowWidget(QMainWindow, MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def start_ui(db):
    global sqlite_db

    sqlite_db = db
    app = QApplication(sys.argv)
    window = MainWindowWidget()
    window.show()
    window.update_results()
    sys.excepthook = except_hook
    sys.exit(app.exec())
