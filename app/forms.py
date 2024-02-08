from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired

class SearchPokemon(FlaskForm):
    name = StringField('name: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Login(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField('Submit')

class Signup(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField('Submit')