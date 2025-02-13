import functools

from flask import render_template, redirect, request, url_for, flash, session
from workfuel import app, db
from workfuel.forms import LoginForm, RegistrationForm, DataForm, SettingsForm
from workfuel.logger import logger
from workfuel.models import User, WorkTime, Locomotive, Fuel, Settings
from workfuel.utils import get_monthly_work_time, existing_work_time
from workfuel.helpers import validate_settings_form, validate_create_work_form, validate_register_form, validate_data_form
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta


def log_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Ошибка в {func.__name__}: {str(e)}", exc_info=True)
            from flask import request
            if request:
                return render_template("error.html"), 500
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

    date_str = request.form.get('date', '').strip()
    start_of_work_str = request.form.get('start_of_work', '').strip()
    end_of_work_str = request.form.get('end_of_work', '').strip()

    route_number = request.form.get('route_number', '').strip()
    locomotive_number = request.form.get('locomotive_number', '').strip()
    beginning_fuel_liters = request.form.get('beginning_fuel_liters', '').strip()
    end_fuel_litres = request.form.get('end_fuel_litres', '').strip()
    specific_weight = request.form.get('specific_weight', '').strip()
    norm = request.form.get('norm', '').strip()

    errors = validate_create_work_form(date_str, route_number, locomotive_number, start_of_work_str,
                                       end_of_work_str, beginning_fuel_liters,
                                       end_fuel_litres, specific_weight, norm
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
                              end_fuel_litres, specific_weight
           ):
        return render_template('data_form.html', data_form=data_form)

    try:
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
            specific_weight=specific_weight,
            norm=float(norm),
            fact=fact,
            locomotive_id=new_locomotive.id
        )
        db.session.add(new_fuel)
        db.session.commit()

        flash('Смена успешно создана', 'success')
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
