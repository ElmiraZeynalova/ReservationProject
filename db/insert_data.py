import sqlite3
from backend.db.config import DB_NAME

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

users = [
            ("Jamie Smith", "1-820-334-0249"),
            ("Ashley Watts", "1-444-405-4648"),
            ("Alexander Harvey", "1-947-391-1153"),
            ("Shane Austin", "1-773-729-5012"),
            ("Lionel Parker", "1-903-129-7842")
        ]

tables = [
            (1, 4, "free"),
            (2, 2, "reserved"),
            (3, 6, "free"),
            (4, 2, "reserved"),
            (5, 2, "reserved")
        ]

reservations = [
                    (1, 2, "2025-04-02 18:00"),
                    (2, 1, "2025-04-02 19:30"),
                    (3, 3, "2025-04-03 12:00"),
                    (4, 4, "2025-04-03 15:00"),
                    (5, 5, "2025-04-04 20:00")
                ]

cursor.executemany("INSERT INTO User (fullname, phone) VALUES (?, ?)", users)
cursor.executemany("INSERT INTO Tables (number, seats, status) VALUES (?, ?, ?)", tables)
cursor.executemany("INSERT INTO Reservation (table_id, user_id, time) VALUES (?, ?, ?)", reservations)

connection.commit()
connection.close()