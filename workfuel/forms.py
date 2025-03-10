from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, DateTimeField, \
    DateTimeLocalField, \
    SelectMultipleField, SelectField, DecimalField
from wtforms.validators import DataRequired, Optional, EqualTo, Length


class LoginForm(FlaskForm):
    personnel_number = IntegerField('Personnel number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional(), Length(min=2, max=25)],
                             render_kw={'placeholder': 'Введите имя 2-25 символов (необязательно)'})
    last_name = StringField('Last Name', validators=[Optional(), Length(min=2, max=25)],
                            render_kw={'placeholder': 'Введите фамилию 2-25 символов (необязательно)'})
    personnel_number = IntegerField('Personnel number', validators=[DataRequired()],
                                    render_kw={'placeholder': 'Введите табельный номер "_____"'})
    password = PasswordField('Password', validators=[DataRequired(message='Пароль должен быть не менее 3-х символов')],
                             render_kw={'placeholder': 'Создайте пароль не менее 3 символов'})
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password',
                                                                                                 message='Пароли должны совпадать')])
    submit = SubmitField('Register')


class MainDataForm(FlaskForm):
    start_of_work = DateTimeLocalField('Start work', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    end_of_work = DateTimeLocalField('End work', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    route_number = IntegerField('Route number', validators=[DataRequired()],
                                render_kw={'placeholder': 'Введите номер маршрута состоящий из семи цифр'})
    locomotive_number = IntegerField('Locomotive', validators=[DataRequired()],
                                     render_kw={'placeholder': 'Введите номер тепловоза'})


class AdditionalDataForm(FlaskForm):
    work_park = SelectField('Рабочий парк', choices=[('park1', 'Парк 1'), ('park2', 'Парк 2')],
                            validators=[DataRequired()])
    work_time = DecimalField('Время работы в парке (часы)', validators=[DataRequired()])
    reserve_section = SelectField('Резервный пробег', choices=[('section1', 'Участок 1'), ('section2', 'Участок 2')],
                                  validators=[DataRequired()])
    reserve_time = DecimalField('Общее время на резервный пробег (часы)', validators=[DataRequired()])
    start_fuel_litres = DecimalField('Дизельное топливо (принял)', validators=[DataRequired()],
                                     render_kw={'placeholder': 'Введите объём дизельного топлива в литрах'})
    end_fuel_litres = DecimalField('Дизельное топливо (сдал)', validators=[DataRequired()],
                                   render_kw={'placeholder': 'Введите объём дизельного топлива в литрах'})
    specific_weight = DecimalField('Удельный вес топлива', validators=[DataRequired()],
                                   render_kw={'placeholder': 'Введите переводной коэффициент: 0.___'})
    add_fuel = StringField('Экипировка', validators=[DataRequired()],
                            render_kw={'placeholder': 'Введите количество топлива в литрах (если была экипировка)'})
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
    park_tch_8_norm = FloatField('Park TCH-8 norm', validators=[DataRequired()])
    park_dnepr_norm = FloatField('Park Dnepr norm', validators=[DataRequired()])
    park_gorvetka_norm = FloatField('Park Gorvetka norm', validators=[DataRequired()])
    park_diyovka_norm = FloatField('Park Diyovka norm', validators=[DataRequired()])
    park_gorainovo_norm = FloatField('Park Goryainovo norm', validators=[DataRequired()])
    park_kaidakskaya_norm = FloatField('Park Kaidakskaya norm', validators=[DataRequired()])
    park_nizhnedneprovsk_norm = FloatField('Park Nizhnedneprovsk norm', validators=[DataRequired()])
    park_pristan_norm = FloatField('Park Pristan norm', validators=[DataRequired()])
    park_lotsmanka_norm = FloatField('Park Lotsmanka norm', validators=[DataRequired()])
    park_vstrechnyy_norm = FloatField('Park Vstrechnyy norm', validators=[DataRequired()])
    park_dn_gruzovoy_norm = FloatField('Park Dn Gruzovoy norm', validators=[DataRequired()])
    park_obvodnaya_norm = FloatField('Park Obvodnaya norm', validators=[DataRequired()])
    park_lisky_norm = FloatField('Park Lisky norm', validators=[DataRequired()])
    park_privolnoe_norm = FloatField('Park Privolnoe norm', validators=[DataRequired()])
    park_rasnaya_norm = FloatField('Park Rasnaya norm', validators=[DataRequired()])
    park_suhachovka_norm = FloatField('Park Suhacovka norm', validators=[DataRequired()])
    hot_state = IntegerField('Hot state', validators=[DataRequired()])
    cool_state = IntegerField('Cool state', validators=[DataRequired()])
    submit = SubmitField('Edit')
