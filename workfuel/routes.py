from flask import render_template,redirect, request, url_for, flash, session
from workfuel import app, db
from workfuel.forms import LoginForm, RegistrationForm
from workfuel.models import User, WorkTime, Locomotive, Fuel
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/')
def return_main_page():
    return render_template('main_page.html')


@app.route('/profile')
def return_profile():
    user_id = session.get('user_id')
    locomotive_id = session.get('locomotive_id')
    if user_id:
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            date_of_work = WorkTime.filter_by(owner=user_id).all()
            locomotive = Locomotive.filter_by(owner=user_id).first()
            fuel_data = Fuel.filter_by(owner=locomotive_id).all()
            specific_weight = Fuel.filter_by()

            combined_data = [
                {
                    'date': date_of_work,
                    'locomotive': locomotive,
                    'beginning_fuel_liters': beginning_fuel_liters,
                    'end_fuel_litres': end_fuel_litres,
                    'specific_weight': specific_weight
                }
                for date, locomotive, beginning_fuel_liters, end_fuel_litres, specific_weight in zip(
                date_of_work, locomotive, fuel_data, specific_weight
                )
            ]

            return render_template('profile.html', user=user, combined_data=combined_data)
        else:
            flash('Нужно войти в систему', 'danger')
            return redirect('login_user_get')


@app.route('/login', methods=['GET'])
def login_user_get():
    login_form = LoginForm(request.form)
    return render_template('login_register.html', login_tab=True, login_form=login_form)


@app.route('/login', methods=['POST'])
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
    return redirect(url_for("login_user_get"))


@app.route('/register', methods=['GET'])
def register_user_get():
    registration_form = RegistrationForm(request.form)
    return render_template('login_register.html', register_tab=True, registration_form=registration_form)


@app.route('/register', methods=['POST'])
def register_user_post():
    registration_form = RegistrationForm(request.form)

    if registration_form.validate_on_submit():
        first_name = registration_form.first_name.data
        last_name = registration_form.last_name.data
        personnel_number = registration_form.personnel_number.data
        password = registration_form.password.data
        email = registration_form.email.data

        if User.query.filter_by(personnel_number=personnel_number).first() is not None:
            flash('Такой ник уже существует','danger')
            return render_template('login_register.html', registration_form=registration_form)

        if User.query.filter_by(email=email).first() is not None:
            flash('Такой мэйл уже существует', 'danger')
            return render_template('login_register.html', registration_form=registration_form)

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            personnel_number=personnel_number,
            password=generate_password_hash(password),
            email=email
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
        return render_template('login_register.html', registration_form=registration_form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login_user_get'))


