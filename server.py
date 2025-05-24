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
    party_size = SelectField('Number of guests', validators=[DataRequired()], choices=[(str(i), i) for i in range(1, 9)])
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


        return redirect(url_for('select_time', date=date, party_size=party_size, time=time))

    return render_template('index.html', reservation_form=form, alternatives=alternatives)


@app.route('/select_time', methods=['GET'])
def select_time():
    date_str = request.args.get('date')
    party_size = int(request.args.get('party_size'))
    time = request.args.get('time')
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format', 'danger')
        return redirect(url_for('index'))
    
    available_times = get_available_times(date, time, party_size)
    
    return render_template('select_time.html', 
                           date=date_str, 
                           party_size=party_size, 
                           available_times=available_times)


@app.route('/check_availability', methods=['POST'])
def check_availability():
    data = request.json
    date = datetime.strptime(data['date'], "%Y-%m-%d").date()
    time = data['time']
    party_size = int(data['party_size'])

    available_times = get_available_times(date, time, party_size)
    
    result = {
        'available': len(available_times) > 0,
        'times': available_times
    }

    return jsonify(result)


@app.route('/confirm_reservation/<date>/<time>/<party_size>', methods=['GET', 'POST'])
def confirm_reservation(date, time, party_size):
    form = ConfirmReservationForm()
    
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        party_size_int = int(party_size)
    except ValueError:
        flash('Invalid parameters', 'danger')
        return redirect(url_for('index'))
    
    available_table = Table.query.filter(
        Table.seats >= party_size_int,
        Table.status == 'available'
    ).filter(~Table.id.in_(
        db.session.query(Reservation.table_id).filter_by(date=date_obj, time=time)
    )).first()
    
    if not available_table:
        flash('Sorry, this time is no longer available', 'danger')
        return redirect(url_for('index'))
    
    if form.validate_on_submit():
        fullname = form.fullname.data
        phone = form.phone.data
        email = form.email.data

        # Создаем пользователя
        user = User(fullname=fullname, phone=phone, email=email)
        db.session.add(user)
        db.session.commit()

        # Создаем бронирование
        reservation = Reservation(
            user_id=user.id,
            table_id=available_table.id,
            date=date_obj,
            time=time
        )
        db.session.add(reservation)
        available_table.status = 'reserved'
        db.session.commit()

        flash('Reservation confirmed!', 'success')
        return redirect(url_for('index'))

    return render_template('confirm_reservation.html', 
                          form=form, 
                          date=date, 
                          time=time, 
                          party_size=party_size,
                          table_id=available_table.id if available_table else None)


def get_available_times(date, time_str, party_size):
  
    time_obj = datetime.strptime(time_str, "%H:%M")
    available_times = []
    

    available_table = check_time_available(date, time_str, party_size)
    if available_table:
        available_times.append({
            'time': time_str,
            'table_id': available_table.id,
            'is_original': True
        })
    
  
    minus_30 = (time_obj - timedelta(minutes=30)).strftime("%H:%M")
    available_table = check_time_available(date, minus_30, party_size)
    if available_table:
        available_times.append({
            'time': minus_30,
            'table_id': available_table.id,
            'is_original': False
        })
    

    plus_30 = (time_obj + timedelta(minutes=30)).strftime("%H:%M")
    available_table = check_time_available(date, plus_30, party_size)
    if available_table:
        available_times.append({
            'time': plus_30,
            'table_id': available_table.id,
            'is_original': False
        })
    
    return available_times


def check_time_available(date, time_str, party_size):

    available_table = Table.query.filter(
        Table.seats >= party_size,
        Table.status == 'available'
    ).filter(~Table.id.in_(
        db.session.query(Reservation.table_id).filter_by(date=date, time=time_str)
    )).first()
    
    return available_table


if __name__ == '__main__':
    app.run(debug=True)