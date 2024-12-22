# location_app/products/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, URL

class ProductForm(FlaskForm):
    name = StringField('Nom du produit', validators=[DataRequired(), Length(min=2, max=128)])
    daily_price = FloatField('Prix quotidien (€)', validators=[DataRequired(), NumberRange(min=0)])
    image_url = URLField('URL de l\'image', validators=[Optional(), URL(message='Veuillez entrer une URL valide.')])  # **Nouveau champ pour l'URL de l'image**
    submit = SubmitField('Enregistrer')
