from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField, StringField
from wtforms.validators import DataRequired, Email
from datetime import datetime, timedelta
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from database import db, User, Table, Reservation
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'j3R7l#@kd!o9z$%v3Q2p8yB1mLx7WkzN'  
db_name = 'reservation.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
bootstrap = Bootstrap5(app)  


class ReservationForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    party_size = SelectField('Number of guests', validators=[DataRequired()], choices=[(str(i), i) for i in range(1, 11)])
    time = SelectField('Time', validators=[DataRequired()], choices=[
        ('08:00', '08:00'),('08:30', '08:30'),('09:00', '09:00'),('09:30', '09:30'),('10:00', '10:00'),('10:30', '10:30'),('11:00', '11:00'),('11:30', '11:30'),('12:00', '12:00'),('12:30', '12:30'),('13:00', '13:00'),('13:30', '13:30'),('14:00', '14:00'), ('14:30', '14:30'),('15:00', '15:00'),('15:30', '15:30'),('16:00', '16:00'),('16:30', '16:30'),('17:00', '17:00'),('17:30', '17:30'),('18:00', '18:00'), ('18:30', '18:30'), ('19:00', '19:00'),
        ('19:30', '19:30'), ('20:00', '20:00'), ('20:30', '20:30'),
        ('21:00', '21:00')
    ])
    submit = SubmitField('Search')


class ConfirmReservationForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Complete Reservation')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ReservationForm()
    alternatives = []

    if request.method == 'POST' and form.validate_on_submit():
        date = form.date.data
        party_size = int(form.party_size.data)
        time = form.time.data

        reservation_datetime = datetime.combine(date, datetime.strptime(time, "%H:%M").time())
        available_table = Table.query.filter(
            Table.seats >= party_size,
            Table.status == 'available'
        ).filter(~Table.id.in_(
            db.session.query(Reservation.table_id).filter(
                Reservation.date == date,
                Reservation.time == time
            )
        )).first()

        if available_table:
            flash('Time is available. Confirm to book.', 'success')
        else:
            alternatives = get_alternative_times(date, time, party_size)
            if alternatives:
                flash(f'No availability at {time}, but available at:', 'warning')
            else:
                flash('No available tables at this time or nearby.', 'danger')

    return render_template('index.html', reservation_form=form, alternatives=alternatives)


@app.route('/check_availability', methods=['POST'])
def check_availability():
    data = request.json
    date = datetime.strptime(data['date'], "%Y-%m-%d").date()
    time = data['time']
    party_size = int(data['party_size'])

    available = Table.query.filter(
        Table.seats >= party_size,
        Table.status == 'available'
    ).filter(~Table.id.in_(
        db.session.query(Reservation.table_id).filter_by(date=date, time=time)
    )).first()

    if available:
        result = {
            'available': True,
            'times': [time],
            'table_id': available.id  # Возвращаем table_id
        }
    else:
        alternatives = get_alternative_times(date, time, party_size)
        result = {
            'available': False,
            'times': alternatives,
            'table_id': None  # Если нет доступных столов
        }

    return jsonify(result)


@app.route('/confirm_reservation', methods=['GET', 'POST'])
def confirm_reservation():
    form = ConfirmReservationForm()
    if form.validate_on_submit():
        # Получаем данные из формы
        fullname = form.fullname.data
        phone = form.phone.data
        email = form.email.data
        table_id = request.form.get('table_id')
        date = request.form.get('date')
        time = request.form.get('time')

        # Создаем нового пользователя
        user = User(fullname=fullname, phone=phone, email=email)
        db.session.add(user)
        db.session.commit()

        # Создаем новую запись бронирования
        reservation = Reservation(
            user_id=user.id,
            table_id=table_id,
            date=datetime.strptime(date, '%Y-%m-%d').date(),
            time=time
        )
        db.session.add(reservation)

        # Обновляем статус стола
        table = Table.query.get(table_id)
        if table:
            table.status = 'reserved'
            db.session.commit()

        return redirect(url_for('index'))

    # Передаем форму в шаблон
    return render_template('confirm_reservation.html', form=form)


def get_alternative_times(date, time_str, party_size):
    time_obj = datetime.strptime(time_str, "%H:%M")
    deltas = [-30, 30]  
    alternatives = []

    for delta in deltas:
        alt_time = (time_obj + timedelta(minutes=delta)).time()
        alt_time_str = alt_time.strftime("%H:%M")
        available = Table.query.filter(
            Table.seats >= party_size,
            Table.status == 'available'
        ).filter(~Table.id.in_(
            db.session.query(Reservation.table_id).filter_by(date=date, time=alt_time_str)
        )).first()
        if available:
            alternatives.append(alt_time_str)


if __name__ == '__main__':
    app.run(debug=True)
