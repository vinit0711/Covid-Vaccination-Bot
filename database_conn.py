import sqlite3


def create_conn():
    conn = sqlite3.connect('VaccineBooking.db')
    c = conn.cursor()
    c.execute('''
               CREATE TABLE IF NOT EXISTS VaccineBooking(
                user_name INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                Location TEXT NOT NULL,
                Category TEXT NOT NULL UNIQUE,
                Date DATE NOT NULL UNIQUE,
                Slots TEXT NOT NULL UNIQUE
              )
              ''')
    conn.commit()
