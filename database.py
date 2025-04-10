from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    reservations = db.relationship('Reservation', backref='user', lazy=True)

class Table(db.Model):
    __tablename__ = 'tables'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    seats = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # наприклад: "available", "reserved"

    reservations = db.relationship('Reservation', backref='table', lazy=True)

class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    time = db.Column(db.String(10), nullable=False)  # наприклад: "18:00"
    date = db.Column(db.Date, nullable=False)


