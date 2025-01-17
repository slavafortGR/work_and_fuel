from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, IntegerField, FloatField
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
    date = StringField('Date', validators=[DataRequired()])
    route_number = IntegerField('Route number', validators=[DataRequired()])
    start_of_work = FloatField('Start work', validators=[DataRequired()])
    end_of_work = FloatField('End work', validators=[DataRequired()])
    locomotive_number = StringField('Locomotive', validators=[DataRequired()])
    beginning_fuel_liters = IntegerField('Beginning Fuel Liters', validators=[DataRequired()])
    end_fuel_litres = FloatField('End Fuel Litres', validators=[DataRequired()])
    specific_weight = FloatField('Specific Weight', validators=[DataRequired()])
