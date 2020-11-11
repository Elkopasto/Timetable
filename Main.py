import sqlite3


def connect():
    try:
        return sqlite3.connect('Timetable.sqlite')
    except Exception as e:
        print(e)


def addTeacher(con=None, **items):
    try:
        con.execute(f"INSERT INTO teachers ({', '.join(items)}) VALUES({', '.join(items.values())})")
    except ValueError:
        print('Connection = NONE')
    except Exception as e:
        print(e)

def addSubjbect(con=None, **items):
    try:
        con.execute(f"INSERT INTO subjects ({', '.join(items)}) VALUES({', '.join(items.values())})")
    except ValueError:
        print('Connection = NONE')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    con = connect()
    cur = con.cursor()
    for i in 'математика, алгебра, геометрия, история, география, экономика,' \
             'физика, химия, биология, обществознание, русскиий язык, литература,' \
             'английский, иностранный язык, труд, технология, чертчение, спорт, IT'.split(', '):
        addSubjbect(con, title=f"'{i}'")
    con.commit()