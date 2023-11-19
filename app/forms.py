from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit_btn = SubmitField('Login')
    
class SignupForm(FlaskForm):
    first_name = StringField('First Name: ', validators=[DataRequired()])
    last_name = StringField('Last Name: ', validators=[DataRequired()])
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password')])
    submit_btn = SubmitField('Register')

class Get_Poke_Info(FlaskForm):
    pokemon_name = StringField('Pokemon Name: ', validators=[DataRequired()])
    submit_btn = SubmitField('Catch')
    
class BattleForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Battle')