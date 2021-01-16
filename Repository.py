import sqlite3
import atexit

from DAO import _DAO


class _Repository:
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.DAO = _DAO(self.conn)

    def close(self):
        self.conn.commit()
        self.conn.close()

    def create_tables(self):
        self.conn.execute("""CREATE TABLE Logistics(id INTEGER PRIMARY KEY,
                            name STRING NOT NULL,
                            count_sent INTEGER NOT NULL,
                            count_received INTEGER NOT NULL)
                            """)
        self.conn.execute("""CREATE TABLE Suppliers(id INTEGER PRIMARY KEY,
                            name STRING NOT NULL,
                            logistic INTEGER NOT NULL,
                            FOREIGN KEY(logistic) REFERENCES Logistics(id))
                            """)
        self.conn.execute("""CREATE TABLE Vaccines(id INTEGER PRIMARY KEY,
                            date DATE NOT NULL,
                            supplier INTEGER,
                            quantity INTEGER NOT NULL,
                            FOREIGN KEY(supplier) REFERENCES Suppliers(id))
                            """)
        self.conn.execute("""CREATE TABLE Clinics(id INTEGER PRIMARY KEY,
                            location STRING NOT NULL,
                            demand INTEGER NOT NULL,
                            logistic INTEGER NOT NULL,
                            FOREIGN KEY(logistic) REFERENCES Logistics(id))
                            """)

    def print_table(self, table):
        self.cursor.execute("SELECT * FROM " + table)
        lst = self.cursor.fetchall()
        print(lst)


repo = _Repository("database.db")
atexit.register(repo.close)
