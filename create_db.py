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
    tables = [
        Table(number=1, seats=2, status='available'),
        Table(number=2, seats=2, status='available'),
        Table(number=3, seats=2, status='available'),
        Table(number=4, seats=2, status='available'),
        Table(number=5, seats=4, status='available'),
        Table(number=6, seats=4, status='available'),
        Table(number=7, seats=4, status='available'),
        Table(number=8, seats=6, status='available'),
        Table(number=9, seats=6, status='available'),
        Table(number=10, seats=8, status='available'),
    ]
    db.session.add_all(tables)
    db.session.commit()

    print("Базу даних створено та таблицю заповнено!")
