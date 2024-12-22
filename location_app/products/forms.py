# location_app/products/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Nom du produit', validators=[DataRequired(), Length(min=2, max=128)])
    daily_price = FloatField('Prix quotidien (€)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Enregistrer')
