import sqlite3
from backend.db.config import DB_NAME

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

# User Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
               user_id INTEGER PRIMARY KEY AUTOINCREMENT,
               fullname TEXT NOT NULL,
               phone TEXT UNIQUE NOT NULL
               )
''')

# 'Tables' Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Tables (
                table_id INTEGER PRIMARY KEY AUTOINCREMENT,
                number INTEGER UNIQUE NOT NULL,  
                seats INTEGER NOT NULL,          
                status TEXT NOT NULL CHECK(status IN ('free', 'reserved'))  
                )
''')

# Resesrvation Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Reservation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                time TEXT NOT NULL,  
                FOREIGN KEY (table_id) REFERENCES Tables(id),
                FOREIGN KEY (user_id) REFERENCES User(id)
                )
''')


connection.commit()
connection.close()