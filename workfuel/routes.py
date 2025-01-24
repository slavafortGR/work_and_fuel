from flask import render_template, redirect, request, url_for, flash, session
from workfuel import app, db
from workfuel.forms import LoginForm, RegistrationForm, DataForm
from workfuel.models import User, WorkTime, Locomotive, Fuel
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/')
def return_main_page():
    return render_template('main_page.html')


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
    return redirect(url_for('login_user_get'))


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

        if User.query.filter_by(personnel_number=personnel_number).first() is not None:
            flash('Такой табельный номер уже существует', 'danger')
            return render_template('login_register.html', registration_form=registration_form)

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
        return render_template('login_register.html', registration_form=registration_form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login_user_get'))


@app.route('/profile', methods=['GET'])
def return_profile():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        work_times = WorkTime.query.filter_by(user_id=user_id).all()
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

        return render_template('profile.html', user=user, combined_data=combined_data)

    else:
        flash('Нужно войти в систему', 'danger')
        return redirect('login_user_get')




@app.route('/create', methods=['GET'])
def create_work_form_get():
    data_form = DataForm(request.form)

    if 'user_id' in session:
        return render_template('data_form.html', data_form=data_form)
    flash('You need login', 'danger')
    return redirect(url_for('login_user_get'))


@app.route('/create', methods=['POST'])
def create_work_form_post():
    data_form = DataForm(request.form)

    date = request.form.get('date')
    route_number = request.form.get('route_number')
    start_of_work = request.form.get('start_of_work')
    end_of_work = request.form.get('end_of_work')
    locomotive_number = request.form.get('locomotive_number')
    beginning_fuel_liters = request.form.get('beginning_fuel_liters')
    end_fuel_litres = request.form.get('end_fuel_litres')
    specific_weight = request.form.get('specific_weight')
    norm = request.form.get('norm')
    fact = request.form.get('fact')
    print(norm, fact)

    if data_form.validate_on_submit():
        try:
            new_work_time = WorkTime(
                date=date,
                route_number=route_number,
                start_of_work=start_of_work,
                end_of_work=end_of_work,
                user_id=session['user_id']
            )
            db.session.add(new_work_time)
            db.session.commit()

            new_locomotive = Locomotive(
                locomotive_number=locomotive_number,
                driver=session['user_id']
            )
            db.session.add(new_locomotive)
            db.session.commit()

            new_fuel = Fuel(
                beginning_fuel_liters=beginning_fuel_liters,
                beginning_fuel_kilo=int(beginning_fuel_liters) * float(specific_weight),
                end_fuel_litres=end_fuel_litres,
                end_fuel_kilo=int(end_fuel_litres) * float(specific_weight),
                specific_weight=specific_weight,
                norm=float(norm),
                fact=float(fact),
                locomotive_id=new_locomotive.id
            )
            db.session.add(new_fuel)
            db.session.commit()

            flash('Смена успешно создана', 'success')
            print('Смена успешно создана')
            return redirect(url_for('return_profile'))
        except Exception as e:
            db.session.rollback()
            print('Mistake', {str(e)})

            flash(f'An error occurred: {str(e)}', 'danger')
        return render_template('data_form.html', data_form=data_form)
    else:
        return render_template('data_form.html', data_form=data_form)
