from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchPokemon(FlaskForm):
    name = StringField('name: ', validators=[DataRequired()])
    submit = SubmitField('submit')

