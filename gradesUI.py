from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox

gradesList = [str(i) + ' класс' for i in range(1, 12)]


class GradesView(object):
    def setupUi(self, grades):
        grades.setWindowTitle("Классы")
        grades.setObjectName("Grades")
        grades.resize(789, 650)

        self.grade = -1

        self.centralwidget = QtWidgets.QWidget(grades)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 50, 771, 431))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.error = QtWidgets.QLabel(self.centralwidget)
        self.error.setEnabled(False)
        self.error.setGeometry(QtCore.QRect(10, 580, 771, 16))
        self.error.setText("")
        self.error.setObjectName("error")

        self.teachers = QtWidgets.QLabel(self.centralwidget)
        self.teachers.setGeometry(QtCore.QRect(10, 490, 121, 16))
        self.teachers.setObjectName("label_2")
        self.teachers.setText('Учителя:')

        self.subject_ids = {i: j for j, i in
                            enumerate([i[0] for i in self.sqlite_db.request("SELECT title FROM subjects")])}

        self.subject_selector = QtWidgets.QComboBox(self.centralwidget)
        self.subject_selector.setGeometry(QtCore.QRect(50, 510, 141, 22))
        self.subject_selector.setObjectName("subject_selector")
        self.subject_selector.addItems(self.subject_ids.keys())

        self.add = QtWidgets.QToolButton(self.centralwidget)
        self.add.setGeometry(QtCore.QRect(200, 510, 21, 21))
        self.add.setObjectName("add")
        self.add.clicked.connect(self.add_lesson)
        self.add.setText('+')

        self.set = QtWidgets.QToolButton(self.centralwidget)
        self.set.setGeometry(QtCore.QRect(350, 560, 21, 21))
        self.set.setObjectName("add")
        self.set.setText('<')
        self.set.clicked.connect(self.set_amount)

        self.grade_selector = QtWidgets.QComboBox(self.centralwidget)
        self.grade_selector.setGeometry(QtCore.QRect(60, 10, 181, 22))
        self.grade_selector.setObjectName("grade_selector")
        self.grade_selector.addItems(gradesList)
        self.grade_selector.currentIndexChanged.connect(self.update_results)

        self.gradeLabel = QtWidgets.QLabel(self.centralwidget)
        self.gradeLabel.setGeometry(QtCore.QRect(10, 10, 61, 16))
        self.gradeLabel.setObjectName("label")
        self.gradeLabel.setText('Класс:')

        self.lesson = QtWidgets.QLabel(self.centralwidget)
        self.lesson.setGeometry(QtCore.QRect(10, 510, 41, 20))
        self.lesson.setObjectName("lesson")
        self.lesson.setText('Урок:')

        self.lesson_2 = QtWidgets.QLabel(self.centralwidget)
        self.lesson_2.setGeometry(QtCore.QRect(10, 560, 41, 20))
        self.lesson_2.setObjectName("lesson_2")
        self.lesson_2.setText('Урок:')

        grade = self.grade_selector.currentIndex() + 1
        self.selected_subjects = [i[0] for i in
                                  self.sqlite_db.request("SELECT title from grades_and_subjects JOIN subjects ON "
                                                         f"id = subject WHERE grade = {grade}")]

        self.subject_selector_2 = QtWidgets.QComboBox(self.centralwidget)
        self.subject_selector_2.setGeometry(QtCore.QRect(50, 560, 141, 22))
        self.subject_selector_2.setObjectName("subject_selector")
        self.subject_selector_2.addItems(self.selected_subjects)

        self.spin_box = QtWidgets.QSpinBox(self.centralwidget)
        self.spin_box.setGeometry(QtCore.QRect(200, 560, 141, 22))
        self.spin_box.setObjectName("subject_selector")

        self.edit_amount = QtWidgets.QLabel(self.centralwidget)
        self.edit_amount.setGeometry(QtCore.QRect(10, 540, 121, 16))
        self.edit_amount.setObjectName("edit_amount")
        self.edit_amount.setText("Задать кол-во")

        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(690, 10, 91, 24))
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.clicked.connect(self.delete_lessons)
        self.deleteButton.setText('Удалить уроки')

        self.refresh = QtWidgets.QPushButton(self.centralwidget)
        self.refresh.setGeometry(QtCore.QRect(620, 510, 75, 24))
        self.refresh.setObjectName("refresh")
        self.refresh.clicked.connect(self.update_results)
        self.refresh.setText('Обновить')

        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearButton.setGeometry(QtCore.QRect(700, 510, 75, 24))
        self.clearButton.setObjectName("clearButton")
        self.clearButton.clicked.connect(self.delete_all)
        self.clearButton.setText('Очистить')

        grades.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(grades)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 789, 21))
        self.menubar.setObjectName("menubar")
        grades.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(grades)
        self.statusbar.setObjectName("statusbar")
        grades.setStatusBar(self.statusbar)

        self.update_results()

    def update_results(self):
        grade = self.grade_selector.currentIndex() + 1

        res = self.sqlite_db.request(
            f"""SELECT title, subject_in_week FROM grades_and_subjects JOIN subjects ON subject = id
            WHERE grade = {grade}""")

        self.tableWidget.setRowCount(len(res))

        if not res:
            self.error.setText('Ничего не найдено')
            self.update_selectors()
            return
        else:
            self.error.setText('')

        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setHorizontalHeaderLabels(['Предмет', 'Кол-во в неделю'])
        self.titles = [description[0] for description in self.sqlite_db.get_cur().description]

        for i, element in enumerate(res):
            for j, val in enumerate(element):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))

        self.update_selectors()

    def update_selectors(self):
        self.grade = self.grade_selector.currentIndex() + 1
        self.subject_selector_2.clear()
        self.selected_subjects = [i[0] for i in
                                  self.sqlite_db.request("SELECT title from grades_and_subjects JOIN subjects ON "
                                                         f"id = subject WHERE grade = {self.grade}")]
        self.subject_selector_2.addItems(self.selected_subjects)

    def add_lesson(self):
        lessons_sum = self.sqlite_db.request(
            f"SELECT SUM(subject_in_week) FROM grades_and_subjects WHERE grade = {self.grade}")[0][0]
        if lessons_sum is not None and lessons_sum >= 30:
            self.error.setText('Макс количество уроков в неделю')
            return

        subject = self.subject_selector.currentIndex()

        res = self.sqlite_db.request(f"""INSERT INTO grades_and_subjects(grade, subject)
        VALUES({self.grade}, {subject})""")

        if res:
            self.error.setText('При добавлении произошла ошибка')
            return
        else:
            self.sqlite_db.commit()
            self.error.setText('')

        self.update_results()

    def set_amount(self):
        amount = int(self.spin_box.text())
        subj = self.subject_ids.get(self.subject_selector_2.currentText())
        lessons_sum = self.sqlite_db.request(
            f"SELECT SUM(subject_in_week) FROM grades_and_subjects"
            f" WHERE grade = {self.grade} AND subject != {subj}")[0][0]

        if amount == 0:
            self.error.setText('Вы не можете поставить нулевое значение')
            return

        if lessons_sum is not None and lessons_sum + amount > 30:
            self.error.setText('Кол-во уроков больше 30')
            return

        res = self.sqlite_db.request(f"UPDATE grades_and_subjects SET subject_in_week = {amount}"
                                     f" WHERE grade = {self.grade} AND subject = {subj}")

        if res:
            self.error.setText('При добавлении произошла ошибка')
            return
        else:
            print('aaa')
            self.sqlite_db.commit()
            self.error.setText('')

        self.update_results()

    def delete_lessons(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [str(self.subject_ids.get(self.tableWidget.item(i, 0).text())) for i in rows]

        if not ids:
            self.error.setText('Предметы не выбраны')
            return

        valid = QMessageBox.question(
            self, '', f"Действительно удалить предметы {', '.join(self.tableWidget.item(i, 0).text() for i in rows)}?",
            QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            self.sqlite_db.request(f'DELETE FROM grades_and_subjects'
                                   f' WHERE grade = {self.grade}'
                                   f' AND subject in ({", ".join(ids)})')
            self.sqlite_db.commit()

        self.error.setText('')
        self.update_results()

    def delete_all(self):
        valid = QMessageBox.question(
            self, '', f"Действительно удалить все предметы в {self.grade} классе?",
            QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            self.sqlite_db.request('DELETE FROM grades_and_subjects'
                                   f' WHERE grade = {self.grade}')
            self.sqlite_db.commit()

        self.error.setText('')
        self.update_results()


class GradesWindowWidget(QMainWindow, GradesView):
    def __init__(self, sqlite_db):
        super().__init__()
        self.sqlite_db = sqlite_db
        self.setupUi(self)
