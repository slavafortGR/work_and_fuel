import functools

from flask import render_template, redirect, request, url_for, flash, session
from workfuel import app, db
from workfuel.forms import LoginForm, RegistrationForm, DataForm, SettingsForm
from workfuel.logger import logger
from workfuel.models import User, WorkTime, Locomotive, Fuel, Settings, SettingsTrack, WorkPark
from workfuel.utils import get_monthly_work_time, existing_work_time
from workfuel.helpers import validate_settings_form, validate_create_work_form, validate_register_form, \
    validate_data_form, convert_to_decimal_hours, validate_work_time, get_park_norms
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta


def log_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f'Ошибка в {func.__name__}: {str(e)}', exc_info=True)
            from flask import request
            if request:
                return 'Произошла ошибка на сервере', 500
            else:
                raise

    return wrapper


@app.route('/')
@log_exceptions
def return_main_page():
    return render_template('main_page.html')


@app.route('/login', methods=['GET'])
@log_exceptions
def login_user_get():
    login_form = LoginForm(request.form)
    return render_template('login_register.html', login_tab=True, login_form=login_form)


@app.route('/login', methods=['POST'])
@log_exceptions
def login_user_post():
    login_form = LoginForm(request.form)

    if login_form.validate_on_submit():
        personnel_number = login_form.personnel_number.data
        password = login_form.password.data

        user = User.query.filter_by(personnel_number=personnel_number).first()
        if not user or not check_password_hash(user.password, password):
            flash('Неверный логин либо пароль', 'danger')
            return redirect(url_for('login_user_get'))
        else:
            session['user_id'] = user.id
            return redirect(url_for('return_profile'))

    flash('Некорректный ввод данных. Проверьте и введите заново', 'danger')
    return redirect(url_for('login_user_get'))


@app.route('/register', methods=['GET'])
@log_exceptions
def register_user_get():
    registration_form = RegistrationForm(request.form)
    return render_template('login_register.html', register_tab=True, registration_form=registration_form)


@app.route('/register', methods=['POST'])
@log_exceptions
def register_user_post():
    registration_form = RegistrationForm(request.form)

    if registration_form.validate_on_submit():
        first_name = registration_form.first_name.data
        last_name = registration_form.last_name.data
        personnel_number = registration_form.personnel_number.data
        password = registration_form.password.data

        if not validate_register_form(personnel_number, password):
            return render_template('login_register.html', register_tab=True, registration_form=registration_form)

        if User.query.filter_by(personnel_number=personnel_number).first() is not None:
            flash('Такой табельный номер уже существует', 'danger')
            return render_template('login_register.html', register_tab=True, registration_form=registration_form)

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            personnel_number=personnel_number,
            password=generate_password_hash(password)
        )

        try:
            db.session.add(new_user)
            db.session.commit()

            flash('Вы успешно зарегистрировались', 'success')
            return redirect(url_for('login_user_get'))
        except Exception as e:
            db.session.rollback()
            flash(f'Произошла ошибка: {str(e)}', 'danger')
    else:
        flash('Неверные регистрационные данные', 'danger')
        return render_template('login_register.html', register_tab=True, registration_form=registration_form)


@app.route('/logout')
@log_exceptions
def logout():
    session.pop('user_id', None)
    return redirect(url_for('return_main_page'))


@app.route('/profile', methods=['GET'])
@log_exceptions
def return_profile():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        work_times = WorkTime.query.filter_by(user_id=user_id).order_by(WorkTime.start_of_work).all()
        locomotives = Locomotive.query.filter_by(driver=user_id).all()

        fuels = []
        for locomotive in locomotives:
            fuels.extend(Fuel.query.filter_by(locomotive_id=locomotive.id).all())

        combined_data = []
        for work_time, locomotive in zip(work_times, locomotives):
            related_fuels = [fuel for fuel in fuels if fuel.locomotive_id == locomotive.id]
            if related_fuels:
                fuel = related_fuels[0]
                combined_data.append({
                    'date': work_time.date,
                    'route_number': work_time.route_number,
                    'locomotive_number': locomotive.locomotive_number,
                    'start_of_work': work_time.start_of_work.strftime('%H:%M'),
                    'end_of_work': work_time.end_of_work.strftime('%H:%M'),
                    'beginning_fuel_liters': fuel.beginning_fuel_liters,
                    'beginning_fuel_kilo': fuel.beginning_fuel_kilo,
                    'end_fuel_litres': fuel.end_fuel_litres,
                    'end_fuel_kilo': fuel.end_fuel_kilo,
                    'specific_weight': fuel.specific_weight,
                    'norm': fuel.norm,
                    'fact': fuel.fact
                })
            else:
                combined_data.append({
                    'date': work_time.date,
                    'locomotive_number': locomotive.locomotive_number,
                    'beginning_fuel_liters': None,
                    'end_fuel_litres': None,
                    'specific_weight': None,
                    'norm': None,
                    'fact': None
                })

        total_work_time = get_monthly_work_time(user_id)

        return render_template('profile.html', user=user, combined_data=combined_data, total_work_time=total_work_time)
    else:
        flash('Нужно войти в систему', 'danger')
        return redirect(url_for('login_user_get'))


@app.route('/create', methods=['GET'])
@log_exceptions
def create_work_form_get():
    data_form = DataForm(request.form)

    if 'user_id' in session:
        return render_template('data_form.html', data_form=data_form)
    flash('You need login', 'danger')
    return redirect(url_for('login_user_get'))


@app.route('/create', methods=['POST'])
@log_exceptions
def create_work_form_post():
    user_id = session.get('user_id')
    data_form = DataForm(request.form)

    data_form.activities.choices = [
        (1, 'Парк "Л"'), (2, 'Парк "Г"'), (3, 'Парк "Е"'), (4, 'Парк "З"'),
        (5, 'Парк "Втормет"'), (6, 'Парк "Нижний"'), (7, 'Парк "ВЧД-3"'),
        (8, 'Парк "ТЧ-1"'), (9, 'Парк "ТЧ-8"'), (10, 'Парк "Днепр Главный"'),
        (11, 'Парк "Горветка"'), (12, 'Парк "Диёвка"'), (13, 'Парк "Горяиново"'),
        (14, 'Парк "Кайдакская"'), (15, 'Парк "Нижнеднепровск"'), (16, 'Парк "Н.Д. Пристань"'),
        (17, 'Парк "Лотсманка"'), (18, 'Парк "Встречный"'), (19, 'Парк "Днепр Грузовой"'),
        (20, 'Парк "Обводная"'), (21, 'Парк "Лиски"'), (22, 'Парк "Парк "Привольное"'),
        (23, 'Парк "Рясная"'), (24, 'Парк "Сухачёвка"'), (25, 'Горячий простой'),
        (26, 'Холодный простой')
    ]

    date_str = request.form.get('date', '').strip()
    start_of_work_str = request.form.get('start_of_work', '').strip()
    end_of_work_str = request.form.get('end_of_work', '').strip()
    route_number = request.form.get('route_number', '').strip()
    locomotive_number = request.form.get('locomotive_number', '').strip()
    beginning_fuel_liters = request.form.get('beginning_fuel_liters', '').strip()
    end_fuel_litres = request.form.get('end_fuel_litres', '').strip()
    specific_weight = request.form.get('specific_weight', '').strip()

    errors = validate_create_work_form(date_str, route_number, locomotive_number, start_of_work_str,
                                       end_of_work_str, beginning_fuel_liters,
                                       end_fuel_litres, specific_weight
                                       )

    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('data_form.html', data_form=data_form)

    date = datetime.strptime(date_str, '%Y.%m.%d').date()
    start_of_work = datetime.combine(date, datetime.strptime(start_of_work_str, '%H:%M').time())
    end_of_work = datetime.combine(date, datetime.strptime(end_of_work_str, '%H:%M').time())

    if end_of_work < start_of_work:
        end_of_work += timedelta(days=1)

    if existing_work_time(user_id, start_of_work, end_of_work):
        flash('Смена с такой датой уже существует! Проверьте даты и попробуйте снова.', 'danger')
        return render_template('data_form.html', data_form=data_form)

    if not validate_data_form(route_number, locomotive_number, beginning_fuel_liters,
                              end_fuel_litres, specific_weight):
        return render_template('data_form.html', data_form=data_form)

    if data_form.validate_on_submit():
        park_ids = data_form.activities.data
        work_hours = data_form.work_hours.data.strip().split()

        if len(park_ids) != len(work_hours):
            flash('Ошибка: количество выбранных парков/простоев и введённых часов не совпадает!', 'danger')
            return render_template('data_form.html', data_form=data_form)

        try:
            work_hours = [convert_to_decimal_hours(h) for h in work_hours]

            actual_work_duration = (end_of_work - start_of_work).total_seconds() / 3600
            if sum(work_hours) > actual_work_duration:
                flash('Ошибка: сумма рабочих часов не может превышать фактическую продолжительность смены!', 'danger')
                return render_template('data_form.html', data_form=data_form)

            try:
                validate_work_time(start_of_work_str, end_of_work_str, work_hours)
            except ValueError as e:
                flash(str(e), 'danger')
                return render_template('data_form.html', data_form=data_form)

            settings = Settings.query.first()
            park_norms = get_park_norms(settings)

            norm = 0

            for activity, hours in zip(park_ids, work_hours):
                if 1 <= activity <= 24:
                    norm += park_norms.get(activity, 0) * hours
                elif activity == 25:
                    norm += settings.hot_state * hours
                elif activity == 26:
                    norm += settings.cool_state * hours

                new_work_park = WorkPark(
                    locomotive_id=int(locomotive_number),
                    park_name=activity,
                    work_hours=hours,
                    hot_state=settings.hot_state if activity == 25 else 0,
                    cool_state=settings.cool_state if activity == 26 else 0,
                    norm=norm
                )
                db.session.add(new_work_park)

            new_work_time = WorkTime(
                date=date,
                route_number=int(route_number),
                start_of_work=start_of_work,
                end_of_work=end_of_work,
                user_id=session['user_id']
            )
            db.session.add(new_work_time)
            db.session.commit()

            new_locomotive = Locomotive(
                locomotive_number=int(locomotive_number),
                driver=session['user_id']
            )
            db.session.add(new_locomotive)
            db.session.commit()

            specific_weight = float(specific_weight)
            beginning_fuel_kilo = int(beginning_fuel_liters) * specific_weight
            end_fuel_kilo = int(end_fuel_litres) * specific_weight
            fact = beginning_fuel_kilo - end_fuel_kilo

            new_fuel = Fuel(
                beginning_fuel_liters=int(beginning_fuel_liters),
                beginning_fuel_kilo=beginning_fuel_kilo,
                end_fuel_litres=int(end_fuel_litres),
                end_fuel_kilo=end_fuel_kilo,
                specific_weight=float(specific_weight),
                fact=fact,
                norm=norm,
                locomotive_id=new_locomotive.id
            )
            db.session.add(new_fuel)
            db.session.commit()

            flash(f'Смена успешно создана. Расчётный расход топлива: {round(norm, 2)} кг.', 'success')
            return redirect(url_for('return_profile'))

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при сохранении данных: {str(e)}', 'danger')

    return render_template('data_form.html', data_form=data_form)


@app.route('/settings', methods=['GET'])
@log_exceptions
def get_settings():
    settings_params = Settings.query.first() or Settings()
    settings_form = SettingsForm(obj=settings_params)

    return render_template('settings.html', settings_params=settings_params, settings_form=settings_form)


@app.route('/settings', methods=['POST'])
@log_exceptions
def post_settings():
    settings_form = SettingsForm(request.form)

    try:
        form_data = request.form.to_dict()

        settings_params = Settings.query.first() or Settings()

        for field, value in form_data.items():
            if hasattr(settings_params, field):
                setattr(settings_params, field, float(value))

        if not validate_settings_form(
                settings_params.park_l_norm, settings_params.park_g_norm,
                settings_params.park_e_norm, settings_params.park_z_norm,
                settings_params.park_vm_norm, settings_params.park_nijny_norm,
                settings_params.park_vchd_3_norm, settings_params.park_tch_1_norm,
                settings_params.park_tch_8_norm, settings_params.park_dnepr_norm,
                settings_params.park_gorvetka_norm, settings_params.park_diyovka_norm,
                settings_params.park_gorainovo_norm, settings_params.park_kaidakskaya_norm,
                settings_params.park_nizhnedneprovsk_norm, settings_params.park_pristan_norm,
                settings_params.park_lotsmanka_norm, settings_params.park_vstrechnyy_norm,
                settings_params.park_dn_gruzovoy_norm, settings_params.park_obvodnaya_norm,
                settings_params.park_lisky_norm, settings_params.park_privolnoe_norm,
                settings_params.park_rasnaya_norm, settings_params.park_suhachovka_norm,
                settings_params.hot_state, settings_params.cool_state
        ):
            return render_template('settings.html', settings_form=settings_form)

        db.session.add(settings_params)
        db.session.commit()
        flash('Настройки успешно обновлены', 'success')
        return redirect(url_for('return_profile'))

    except Exception as e:
        flash('Произошла ошибка: ' + repr(e), 'danger')
        return render_template('settings.html', settings_form=settings_form)
