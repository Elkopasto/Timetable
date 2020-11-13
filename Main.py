import sqlite3
import mainUI


class DuplicateException(Exception):
    pass


class SqliteDb:
    def __init__(self, path):
        try:
            self.con = self.connect(path)
            self.cur = self.con.cursor()
        except sqlite3.Error:
            print('Sqlite error occurred')

    def get_con(self):
        return self.con

    def get_cur(self):
        return self.cur

    def add_to_schedule(self, **items):
        try:
            print("INSERT INTO schedule('{0}') VALUES({1})".format(
                "', '".join(items.keys()), ", ".join(map(str, items.values()))))
            self.con.execute("INSERT INTO schedule('{0}') VALUES({1})".format(
                "', '".join(items.keys()), ", ".join(map(str, items.values()))))
            self.con.commit()
            return True
        except sqlite3.Error:
            return False

    def request(self, request):
        try:
            res = self.con.execute(request).fetchall()
            return res
        except Exception as e:
            print('Request error:', e)

    def connect(self, path):
        try:
            return sqlite3.connect(path)
        except Exception as e:
            print('Connection error:', e)


def add_teacher(con=None, **items):
    # if con or items are not given func returns None
    if not con or not items:
        print('Not enough arguments')
        return

    # casting sqlite request to insert new values
    try:
        con.execute(f"INSERT INTO teachers ({', '.join(items)}) VALUES({', '.join(items.values())})")
        con.commit()
    except sqlite3.Error as e:  # returns if sqlite error
        print('Sqlite error: ' + ' '.join(e.args))
    except Exception as e:  # returns if any other case
        print(e)


def add_subject(con=None, title=None):
    # if con or items are not given func returns None
    if not con or not title:
        print('Not enough args')
        return

    # casting sqlite request to insert new subject
    try:
        if sqlite_db.request("""SELECT title FROM subjects WHERE lower(title) = 'математика'""")[0][0] != title:
            con.execute(f"INSERT INTO subjects (title) VALUES('{title.lower()}')")
        else:
            raise DuplicateException
    except DuplicateException:  # returns if there is already item with te same item
        print('Row already exists')
    except sqlite3.Error as e:  # returns if sqlite error
        print('Sqlite error: ' + ' '.join(e.args))
    except Exception as e:  # returns if any other case
        print(e)


def create_class_day(con=None, grade=1, day=0):
    subjects_bank = []
    for subject in sqlite_db.request(f"SELECT subject, subject_day_limit FROM grades_and_subjects WHERE grade = {grade}"):
        subjects_bank += [str(subject[0])] * subject[1]

    teachers = sqlite_db.request("SELECT id, subject_key FROM subjects_to_teachers"
                                 " JOIN teachers on teacher_key = id WHERE"
                                 " subject_key in ({})".format('"' + '", "'.join(subjects_bank) + '"'))

    for hour in lesson_timing:
        for j in subjects_bank:
            subject_teachers = [teacher[0] for teacher in teachers if str(teacher[1]) == j]

            if not subject_teachers:
                continue

            for subject_teacher in subject_teachers:
                action_status = sqlite_db.add_to_schedule(time=hour[0], subj=j, grade=grade,
                                                          teacher=subject_teacher, day=day)
                if action_status:
                    print(teachers, subject_teachers, sep='\n')
                    print(subjects_bank)
                    subjects_bank.remove(j)
                    print(subjects_bank)
                    break
                else:
                    continue
                break


def create_random_schedule(con=None):
    if not con:
        print('Connection is not given')
        return

    pass


if __name__ == "__main__":
    sqlite_db = SqliteDb('Timetable.sqlite')
    con = sqlite_db.get_con()

    lesson_timing = sqlite_db.request("""SELECT * FROM time WHERE id = id""")
    lesson_amount = len(lesson_timing)

    MainUI.start_ui()

    for i in range(1, 3):
        print(f'\n grade {i} \n')
        create_class_day(con, i)
