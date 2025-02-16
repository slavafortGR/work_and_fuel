from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, DateTimeField, SelectMultipleField
from wtforms.validators import DataRequired, Optional, EqualTo, Length


class LoginForm(FlaskForm):
    personnel_number = IntegerField('Personnel number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional(), Length(min=2, max=25)], render_kw={'placeholder': 'Введите имя 2-25 символов (необязательно)'})
    last_name = StringField('Last Name', validators=[Optional(), Length(min=2, max=25)], render_kw={'placeholder': 'Введите фамилию 2-25 символов (необязательно)'})
    personnel_number = IntegerField('Personnel number', validators=[DataRequired()], render_kw={'placeholder': 'Введите табельный номер "XXXXX"'})
    password = PasswordField('Password', validators=[DataRequired(message='Пароль должен быть не менее 3-х символов')], render_kw={'placeholder': 'Создайте пароль не менее 3 символов'})
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    submit = SubmitField('Register')


class DataForm(FlaskForm):
    date = DateTimeField('Date', validators=[DataRequired()], format='%Y.%m.%d', render_kw={'placeholder': 'Введите дату в формате: гггг.мм.дд'})
    route_number = IntegerField('Route number', validators=[DataRequired()], render_kw={'placeholder': 'Введите номер маршрута в формате: XXXXXXX'})
    start_of_work = DateTimeField('Start work', validators=[DataRequired()], format='%H:%M', render_kw={'placeholder': 'Введите время начала смены в формате: чч:мм'})
    end_of_work = DateTimeField('End work', validators=[DataRequired()], format='%H:%M', render_kw={'placeholder': 'Введите время окончания смены в формате: чч:мм'})
    locomotive_number = IntegerField('Locomotive', validators=[DataRequired()], render_kw={'placeholder': 'Введите номер тепловоза (без серии т)'})
    activities = SelectMultipleField('Выберите рабочие парки', choices=[
        (1, 'Парк "Л"'), (2, 'Парк "Г"'), (3, 'Парк "Е"'), (4, 'Парк "З"'),
        (5, 'Парк "Втормет"'), (6, 'Парк "Нижний"'), (7, 'Парк "ВЧД-3"'),
        (8, 'Парк "ТЧ-1"'), (9, 'Горячий прстой'), (10, 'Холодный простой')
    ], coerce=int)
    work_hours = StringField('Отработанное время (ввод через пробел)', validators=[DataRequired()])
    beginning_fuel_liters = IntegerField('Beginning Fuel Liters', validators=[DataRequired()], render_kw={'placeholder': 'Введите объём дизельного топлива в литрах'})
    end_fuel_litres = FloatField('End Fuel Litres', validators=[DataRequired()], render_kw={'placeholder': 'Введите объём дизельного топлива в литрах'})
    specific_weight = FloatField('Specific Weight', validators=[DataRequired()], render_kw={'placeholder': 'Введите переводной коэффициент в формате: 0.XXX или 0.ХХХХ'})
    add_fuel = IntegerField('Add Fuel', render_kw={'placeholder': 'Введите количество топлива в литрах (при экипировке)'})
    submit = SubmitField('Create')


class SettingsForm(FlaskForm):
    park_l_norm = FloatField('Park L norm', validators=[DataRequired()])
    park_g_norm = FloatField('Park G norm', validators=[DataRequired()])
    park_e_norm = FloatField('Park E norm', validators=[DataRequired()])
    park_z_norm = FloatField('Park Z norm', validators=[DataRequired()])
    park_vm_norm = FloatField('Park VM norm', validators=[DataRequired()])
    park_nijny_norm = FloatField('Park Nijny norm', validators=[DataRequired()])
    park_vchd_3_norm = FloatField('Park VCHD norm', validators=[DataRequired()])
    park_tch_1_norm = FloatField('Park TCH-1 norm', validators=[DataRequired()])
    hot_state = IntegerField('Hot state', validators=[DataRequired()])
    cool_state = IntegerField('Cool state', validators=[DataRequired()])
    submit = SubmitField('Edit')
