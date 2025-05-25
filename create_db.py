from flask import Flask
from database import db, Table

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    # Заполнение таблицы Table тестовыми данными
    new_tables = [
        Table(number=1, seats=2, status='available'),
        Table(number=2, seats=2, status='available'),
        Table(number=3, seats=3, status='available'),
        Table(number=4, seats=3, status='available'),
        Table(number=5, seats=4, status='available'),
        Table(number=6, seats=4, status='available'),
        Table(number=7, seats=5, status='available'),
        Table(number=8, seats=5, status='available'),
        Table(number=9, seats=6, status='available'),
        Table(number=10, seats=6, status='available'),
        Table(number=11, seats=7, status='available'),
        Table(number=12, seats=7, status='available'),
        Table(number=13, seats=7, status='available'),
        Table(number=14, seats=8, status='available'),
        Table(number=15, seats=8, status='available'),
        Table(number=16, seats=3, status='available'),
        Table(number=17, seats=3, status='available'),
        Table(number=18, seats=4, status='available'),
        Table(number=19, seats=5, status='available'),
        Table(number=20, seats=6, status='available'),

    ]
    db.session.add_all(new_tables)
    db.session.commit()

    print("Базу даних створено та таблицю заповнено!")
