# location_app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class UserRoleForm(FlaskForm):
    role = SelectField('Rôle', choices=[('client', 'Client'), ('supplier', 'Fournisseur'), ('admin', 'Administrateur')], validators=[DataRequired()])
    submit = SubmitField('Mettre à Jour')
