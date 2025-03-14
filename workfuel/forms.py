from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, DateTimeField, \
    DateTimeLocalField, \
    SelectMultipleField, SelectField, DecimalField, FieldList, FormField
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


class WorkTimeForm(FlaskForm):
    park = StringField('Парк', validators=[DataRequired()])
    time = DecimalField('Время работы (часы)', validators=[DataRequired()])

class ReserveSectionForm(FlaskForm):
    section = StringField('Резервный участок', validators=[DataRequired()])
    time = DecimalField('Время в пути (часы)', validators=[DataRequired()])

class AdditionalDataForm(FlaskForm):
    work_parks = SelectField(
        'Рабочие парки',
         choices=[(1, 'Парк "Л"'), (2, 'Парк "Г"'), (3, 'Парк "Е"'), (4, 'Парк "З"'),
        (5, 'Парк "Втормет"'), (6, 'Парк "Нижний"'), (7, 'Парк "ВЧД-3"'),
        (8, 'Парк "ТЧ-1"'), (9, 'Парк "ТЧ-8"'), (10, 'Парк "Днепр Главный"'),
        (11, 'Парк "Горветка"'), (12, 'Парк "Диёвка"'), (13, 'Парк "Горяиново"'),
        (14, 'Парк "Кайдакская"'), (15, 'Парк "Нижнеднепровск"'), (16, 'Парк "Н.Д. Пристань"'),
        (17, 'Парк "Лоцманка"'), (18, 'Парк "Встречный"'), (19, 'Парк "Днепр Грузовой"'),
        (20, 'Парк "Обводная"'), (21, 'Парк "Лиски"'), (22, 'Парк "Парк "Привольное"'),
        (23, 'Парк "Рясная"'), (24, 'Парк "Сухачёвка"'), (25, 'Горячий простой'),
        (26, 'Холодный простой')],
         validators=[DataRequired()],
         render_kw={'class': 'form-select'}
    )
    work_times = FieldList(FormField(WorkTimeForm), min_entries=1)

    reserve_section = SelectMultipleField(
        'Резервные пробеги',
        choices=[(1, 'Днепр - Нижнеднепровск'), (2, 'Нижнеднепровск - Н.Д.Узел'), (3, 'Н.Д.Узел - Лоцманка'),
                 (4, 'Лоцманка - Встречный'), (5, 'Встречный - Днепр Грузовой' ), (6, 'Днепр Грузовой - Обводная'),
                 (7, 'Обводная - Сухачёвка'), (8, 'Сухачёвка - Диёвка'), (9, 'Диёвка - Горяиново'),
                 (10, 'Горяиново - Днепр Главный'), (11, 'Днепр Грузовой - Лиски'), (12, 'Лиски - Днепр Грузовой'),
                 (13, 'Днепр Главный - Кайдакская'), (14, 'Кайдакская - Днепр Главный'), (15, 'Встречный - Привольное'),
                 (16, 'Привольное - Рясная'), (17, 'Рясная - Привольное'),(18, 'Привольное - Встречный'),
                 (19, 'Днепр Главный - Горяиново'), (20, 'Горяиново - Диёвка'), (21, 'Диёвка - Сухачёвка'),
                 (22, 'Сухачёвка - Обводная'), (23, 'Обводная - Днепр Грузовой'), (24, 'Днепр Грузовой - Встречный'),
                 (25, 'Встречный - Лоцманка'), (26, 'Лоцманка - Н.Д.Узел'), (27, 'Н.Д.Узел - Нижнеднепровск'),
                 (28, 'Нижнеднепровск - Днепр Главный'), (29, 'Нижнеднепровск - Н.Д.Пристань'), (30, 'Н.Д.Пристань - Нижнеднепровск')],
        validators=[DataRequired()])
    reserve_times = FieldList(FormField(ReserveSectionForm), min_entries=1)

    beginning_fuel_liters = DecimalField('Дизельное топливо (принял)', validators=[DataRequired()],
                                         render_kw={'placeholder': 'Введите объём дизельного топлива в литрах'})
    end_fuel_litres = DecimalField('Дизельное топливо (сдал)', validators=[DataRequired()],
                                   render_kw={'placeholder': 'Введите объём дизельного топлива в литрах'})
    specific_weight = DecimalField('Удельный вес топлива', validators=[DataRequired()],
                                   render_kw={'placeholder': 'Введите переводной коэффициент: 0.___'})
    add_fuel = StringField('Экипировка', validators=[DataRequired()],
                           render_kw={'placeholder': 'Введите количество топлива в литрах (если была экипировка)'})
    submit = SubmitField('Создать смену')


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
