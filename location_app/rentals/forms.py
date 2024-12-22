# location_app/rentals/forms.py

from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class RentalForm(FlaskForm):
    days = IntegerField('Nombre de jours', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Louer')
