# location_app/supplier/forms.py

from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField
from wtforms.validators import DataRequired

class UpdateRentalForm(FlaskForm):
    action = HiddenField('Action', validators=[DataRequired()])  # Champ caché pour l'action
    submit = SubmitField('Mettre à Jour')  # Bouton de soumission
