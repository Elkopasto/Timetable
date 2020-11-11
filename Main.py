import sqlite3


def connect():
    try:
        return sqlite3.connect('Timetable.sqlite')
    except Exception as e:
        print(e)


def addField(cur=None, **kwargs):
    try:
        cur.execute(f"INSERT INTO schedule ({', '.join(kwargs)}) VALUES ({', '.join(kwargs.values())})")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    con = connect()
    cur = con.cursor()
    addField(cur, time="'15:00'", subj="'maths'", grade="9", teacher="'Alexander'", room="'A1'", day="0")
    con.commit()