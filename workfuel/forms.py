from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Optional, Email, EqualTo

class LoginForm(FlaskForm):
    nick_name = StringField('Nick name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    nick_name = StringField('Nick Name', validators=[DataRequired(), Email(message='Enter a valid nick name')])
    email = StringField('Email', validators=[DataRequired(), Email(message='Enter a valid email address')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
