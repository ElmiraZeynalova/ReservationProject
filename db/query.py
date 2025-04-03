
import sqlite3
from config import DB_NAME

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()


cursor.execute('''
    DELETE FROM Reservation
''')

connection.commit()
connection.close()