import sqlite3

class DuplicateException(Exception):
    pass


def connect():
    try:
        return sqlite3.connect('Timetable.sqlite')
    except Exception as e:
        print(e)


def addTeacher(con=None, **items):
    # if con or items are not given func returns None
    if con is None or items is None:
        print('Not enough arguments')
        return

    # casting sqlite request to insert new values
    try:
        con.execute(f"INSERT INTO teachers ({', '.join(items)}) VALUES({', '.join(items.values())})")
    except sqlite3.Error as e: # returns if sqlite error
        print('Sqlite error: ' + e)
    except Exception as e: # returns if any other case
        print(e)

def addSubject(con=None, title=None):
    # if con or items are not given func returns None
    if con is None or title is None:
        print('Not enough args')
        return

    # casting sqlite request to insert new subject
    try:
        if sqlRequest(con, """SELECT title FROM subjects WHERE lower(title) = 'математика'""")[0][0] != title:
            con.execute(f"INSERT INTO subjects (title) VALUES('{title.lower()}')")
        else:
            raise DuplicateException
    except DuplicateException: # returns if there is already item with te same item
        print('Row already exists')
    except Sqlite3.Error as e: # returns if sqlite error
        print('Sqlite error: ' + e)
    except Exception as e: # returns if any other case
        print(e)

def sqlRequest(con=None, request=None):
    try:
        res = con.execute(request).fetchall()
        return res
    except Exception as e:
        print(e)

if __name__ == "__main__":
    con = connect()
    cur = con.cursor()