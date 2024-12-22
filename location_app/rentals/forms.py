from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class RentForm(FlaskForm):
    days = IntegerField('Nombre de jours', validators=[DataRequired(), NumberRange(min=1, message='Veuillez entrer un nombre de jours valide.')])
    submit = SubmitField('Louer')
