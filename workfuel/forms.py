from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, DateTimeField
from wtforms.validators import DataRequired, Optional, EqualTo

class LoginForm(FlaskForm):
    personnel_number = StringField('Personnel number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    personnel_number = StringField('Personnel number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class DataForm(FlaskForm):
    date = DateTimeField('Date', validators=[DataRequired()], format='%d.%m.%y')
    route_number = IntegerField('Route number', validators=[DataRequired()])
    start_of_work = DateTimeField('Start work', validators=[DataRequired()], format='%H:%M')
    end_of_work = DateTimeField('End work', validators=[DataRequired()], format='%H:%M')
    locomotive_number = StringField('Locomotive', validators=[DataRequired()])
    beginning_fuel_liters = IntegerField('Beginning Fuel Liters', validators=[DataRequired()])
    end_fuel_litres = FloatField('End Fuel Litres', validators=[DataRequired()])
    specific_weight = FloatField('Specific Weight', validators=[DataRequired()])
    norm = FloatField('norm', validators=[DataRequired()])
    submit = SubmitField('Create')
