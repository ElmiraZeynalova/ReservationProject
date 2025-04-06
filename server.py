from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.secret_key = 'j3R7l#@kd!o9z$%v3Q2p8yB1mLx7WkzN'  
bootstrap = Bootstrap5(app)  
    

class ReservationForm(FlaskForm):
    party_size = SelectField('Party size', choices=[(str(i), f"{i} guests") for i in range(1, 11)], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = SelectField('Time', choices=[
        ('12:00', '12:00 PM'),
        ('13:00', '1:00 PM'),
        ('14:00', '2:00 PM'),
        ('18:00', '6:00 PM'),
        ('19:00', '7:00 PM'),
        ('20:00', '8:00 PM'),
    ], validators=[DataRequired()])
    submit = SubmitField('Search')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ReservationForm()
    if form.validate_on_submit():
        # тут буде логіка збереження бронювання у БД або лист
        flash('Бронювання успішно прийнято!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', reservation_form=form)



if __name__ == '__main__':
    app.run(debug=True)
