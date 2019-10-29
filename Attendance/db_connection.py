#!/usr/bin/python
 
import sqlite3
from sqlite3 import Error
from datetime import datetime
import os
import errno
import csv

def fetch_items():
    database = "pythonsqlite.db"
    conn = create_connection(database)
    cur = conn.cursor()
    statement = "SELECT * FROM scan"
    cur.execute(statement)
    rows = cur.fetchall()
    total = 0
    return total, rows

def fetch_items1():
    database = "pythonsqlite.db"
    conn = create_connection(database)
    cur = conn.cursor()
    statement = "SELECT * FROM students"
    cur.execute(statement)
    rows = cur.fetchall()

    return rows


def create_dir_file(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def export_data():
    try:

        now = datetime.now()

        database = "pythonsqlite.db"

        conn = create_connection(database)
        cur = conn.cursor()

        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        print(tables)

        exceptions_ = ['scan','budget']

        for table in tables:
            table = table[0]
            if table not in exceptions_:

                date_ = now.strftime("%d-%m-%Y-%H-%M")
                data = cur.execute("SELECT * FROM " + str(table))
                csv_name = 'data/data-' + str(date_) + '/table-'+str(table)+'.csv'
                create_dir_file(csv_name)
                with open(csv_name, 'w', newline="") as f:
                    writer = csv.writer(f,delimiter=',')
                    writer.writerows(data)

        return "Success in exporting data!"
    except Exception as e:
        print(e)
        raise

def add_request(student,id_, event, timestamp_):
    database = "pythonsqlite.db"

    # create a database connection
    conn = create_connection(database)

    cur = conn.cursor()


    statement = "SELECT * FROM scan WHERE student=?"
    task = (str(student),)
    cur.execute(statement, task)
    rows = cur.fetchall()

    for row in rows:
        print("EVENT: " + str(event))
        print("ROW: " + str(row[2]))

        if str(row[2]).strip() == str(event).strip():
            print("Matched")
            return False


    #FOR COUNT
    statement = "INSERT INTO scan (student,id_,attendance,timestamp_) VALUES (?,?,?,?)"
    task = (str(student), id_, event, timestamp_)
    cur.execute(statement, task)

    #FOR OWN TABLE
    event = str(event)
    event = event.replace(" ","_")

    statement1 = "CREATE TABLE IF NOT EXISTS " + str(event) + "(student TEXT,id_ TEXT,time_ TEXT)"
    cur.execute(statement1)
    conn.commit()

    statement = "INSERT INTO " + str(event) + "(student,id_,time_) VALUES (?,?,?)"
    task = (str(student), str(id_), timestamp_)
    cur.execute(statement, task)


    conn.commit()
    conn.close()

    return True

def delete_request(student):
    database = "pythonsqlite.db"
    # create a database connection
    conn = create_connection(database)
    cur = conn.cursor()
    statement = "DELETE FROM scan WHERE student=?"
    statement1 = "DELETE FROM students WHERE rfidcode=?"

    task = (str(student),)
    cur.execute(statement, task)
    cur.execute(statement1, task)
    conn.commit()

def clear_scan():
    database = "pythonsqlite.db"
    # create a database connection
    conn = create_connection(database)
    cur = conn.cursor()
    statement = "DELETE FROM scan"
    cur.execute(statement)
    conn.commit()  


def clear_request():
    database = "pythonsqlite.db"

    # create a database connection
    conn = create_connection(database)


    cur = conn.cursor()
    statement = "DROP TABLE scan"
    cur.execute(statement)
    conn.commit()

    statement1 = "CREATE TABLE scan ( student  TEXT,id_ REAL, attendance INTEGER)"
    cur.execute(statement1)
    conn.commit()

    conn.close()

    print('Reset Success!')



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def insert_request(upc, name,attendance, id_):
    #database = "/home/pi/new/db/pythonsqlite.db"
    database = "pythonsqlite.db"
 
    # create a database connection
    conn = create_connection(database)

    cur = conn.cursor()

    statement = "SELECT * FROM students WHERE rfidcode=?"
    task = (str(upc),)
    cur.execute(statement, task)
    row = cur.fetchone()

    if row is not None:
        return "Student Already Exists"

    try:
        statement = "INSERT INTO students (student_name,attendance,id_number,rfidcode) VALUES (?,?,?,?)"
        task = (str(name), int(attendance),id_, str(upc))
        cur.execute(statement, task)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return str(e)

    


def update_budget(budget):
    #database = "/home/pi/new/db/pythonsqlite.db"
    database = "pythonsqlite.db"
 
    # # create a database connection
    # conn = create_connection(database)



    # cur = conn.cursor()
    # statement = "UPDATE budget SET current = ?"
    # task = (str(budget),)
    # cur.execute(statement, task)
    # conn.commit()
    # conn.close()


    print('Event Update Success!')

def fetch_budget():
    #database = "/home/pi/new/db/pythonsqlite.db"
    return "General Assembly"

    # database = "pythonsqlite.db"
    # conn = create_connection(database)
    # cur = conn.cursor()
    # statement = "SELECT * FROM budget"
    # cur.execute(statement)
    # row = cur.fetchone()
    # return row

#ALTER TABLE students ADD rfidcode TEXT NOT NULL;

def search_request(upc):
    #database = "/home/pi/new/db/pythonsqlite.db"
    database = "pythonsqlite.db"
 
    # create a database connection
    conn = create_connection(database)


    
    cur = conn.cursor()
    statement = "SELECT * FROM students WHERE rfidcode=?"
    task = (str(upc),)
    cur.execute(statement, task)
    row = cur.fetchone()

    if row is None:
        return False
    # if row is None:
    #     amount = raw_input("Enter attendance: ")
    #     insert_request(upc, amount)
    #     statement = "SELECT * FROM students WHERE rfidcode=?"
    #     task = (str(upc),)
    #     cur.execute(statement, task)
    #     row = cur.fetchone()
    #     student = row[0]
    #     value = row[2]
    #     return student, value
    try:
       student = row[0]
       value = row[2]
    except Exception as e:
        print(str(e))


    return student, value

def search_request_delete_item(upc):
    #database = "/home/pi/new/db/pythonsqlite.db"
    database = "pythonsqlite.db"
 
    # create a database connection
    conn = create_connection(database)


    
    cur = conn.cursor()
    statement = "SELECT * FROM students WHERE student_name=?"
    task = (str(upc),)
    cur.execute(statement, task)
    row = cur.fetchone()

    if row is None:
        return False
    # if row is None:
    #     amount = raw_input("Enter attendance: ")
    #     insert_request(upc, amount)
    #     statement = "SELECT * FROM students WHERE rfidcode=?"
    #     task = (str(upc),)
    #     cur.execute(statement, task)
    #     row = cur.fetchone()
    #     student = row[0]
    #     value = row[2]
    #     return student, value
    try:
       student = row[0]
       attendance = row[1]
    except Exception as e:
        print(str(e))


    return student, attendance
def search_request_delete(upc):
    #database = "/home/pi/new/db/pythonsqlite.db"
    database = "pythonsqlite.db"
 
    # create a database connection
    conn = create_connection(database)


    
    cur = conn.cursor()
    statement = "SELECT * FROM scan WHERE student=?"
    task = (str(upc),)
    cur.execute(statement, task)
    row = cur.fetchone()

    if row is None:
        cur = conn.cursor()
        statement = "DELETE FROM students WHERE rfidcode=?"
        task = (str(upc),)
        cur.execute(statement, task)
        return False
    # #     amount = raw_input("Enter attendance: ")
    # #     insert_request(upc, amount)
    # #     statement = "SELECT * FROM students WHERE rfidcode=?"
    # #     task = (str(upc),)
    # #     cur.execute(statement, task)
    # #     row = cur.fetchone()
    # #     student = row[0]
    # #     value = row[2]
    # #     return student, value
    try:
       student = row[0]
       attendance = row[2]
       return student, str(attendance)
    except Exception as e:
        print(str(e))


    

def reduce_quantity_scan(upc):
    #UPDATE Products SET Price = Price + 50 WHERE ProductID = 1
    database = "pythonsqlite.db"
 
    # create a database connection
    conn = create_connection(database)


    
    cur = conn.cursor()
    statement = "UPDATE scan SET attendance = attendance-1 WHERE student=?"
    task = (str(upc),)
    cur.execute(statement, task)
    conn.commit()
    conn.close()

    print('Quantity Update on table "Scan" Success')


def reduce_quantity_item(upc):
    #UPDATE Products SET Price = Price + 50 WHERE ProductID = 1
    database = "pythonsqlite.db"
 
    # create a database connection
    conn = create_connection(database)


    
    cur = conn.cursor()
    statement = "UPDATE students SET attendance = attendance-1 WHERE student_name=?"
    task = (str(upc),)
    cur.execute(statement, task)
    conn.commit()
    conn.close()

    print('Quantity Update on table "Item" Success')


def increase_quantity_item(upc):
    #UPDATE Products SET Price = Price + 50 WHERE ProductID = 1
    database = "pythonsqlite.db"
 
    # create a database connection
    conn = create_connection(database)


    
    cur = conn.cursor()
    statement = "UPDATE students SET attendance = attendance+1 WHERE student_name=?"
    task = (str(upc),)
    cur.execute(statement, task)
    conn.commit()
    conn.close()

    print('Quantity Update on table "Item" Success')
#TODO - Increment
#     - Database of 20 products
#     - 
