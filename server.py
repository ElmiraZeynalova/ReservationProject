from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime, timedelta
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from database import db, User, Table, Reservation
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'j3R7l#@kd!o9z$%v3Q2p8yB1mLx7WkzN'  
# change string to the name of your database; add path if necessary
db_name = 'reservation.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
bootstrap = Bootstrap5(app)  



class ReservationForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    party_size = SelectField('Number of guests', validators=[DataRequired()], choices=[(str(i), i) for i in range(1, 11)])
    time = SelectField('Time', validators=[DataRequired()], choices=[
        ('18:00', '18:00'), ('18:30', '18:30'), ('19:00', '19:00'),
        ('19:30', '19:30'), ('20:00', '20:00'), ('20:30', '20:30'),
        ('21:00', '21:00')
    ])
    submit = SubmitField('Search')




@app.route('/', methods=['GET', 'POST'])
def index():
    form = ReservationForm()

    if request.method == 'POST' and form.validate_on_submit():
        date = form.date.data
        party_size = int(form.party_size.data)
        time = form.time.data

        # Перевірка на доступні столики
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
            # Створення нової резервації
            new_reservation = Reservation(
                user_id=1,  # тимчасово, поки немає авторизації
                table_id=available_table.id,
                date=date,
                time=time
            )
            db.session.add(new_reservation)
            db.session.commit()
            flash('Reservation confirmed!', 'success')
        else:
            # Якщо столик недоступний, шукаємо альтернативи
            alternatives = get_alternative_times(date, time, party_size)
            if alternatives:
                flash(f'No availability at {time}, but available at: {", ".join(alternatives)}', 'warning')
            else:
                flash('No available tables at this time or nearby.', 'danger')

        return redirect(url_for('index'))

    return render_template('index.html', reservation_form=form)


def get_alternative_times(date, time_str, party_size):
    time_obj = datetime.strptime(time_str, "%H:%M")
    deltas = [-30, 30]  # ±30 хвилин
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

    return alternatives


if __name__ == '__main__':
    app.run(debug=True)
