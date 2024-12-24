from flask import render_template,redirect, request, url_for, flash, session
from workfuel import app
from workfuel.forms import LoginForm
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/')
def return_main_page():
    return render_template('main_page.html')


@app.route('/profile')
def return_profile():
    user_id = session.get('user_id')
    if user_id:
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            return render_template('profile.html', user=user)
        else:
            flash('Нужно войти в систему', 'danger')
            return redirect('login_user_get')


@app.route('login', method=['GET'])
def login_user_get():
    login_form = LoginForm(request.form)
    return render_template('login_register.html')


@app.route("/login", methods=["POST"])
def login_user_post():
    login_form = LoginForm(request.form)

    if login_form.validate_on_submit():
        nick_name = login_form.nick_name.data
        password = login_form.password.data

        user = User.query.filter_by(nick_name=nick_name).first()
        if not user or not check_password_hash(user.password, password):
            flash('Неверный логин либо пароль', 'danger')
            return redirect(url_for('login_user_get'))
        else:
            session['user_id'] = user.id
            return redirect(url_for('return_profile'))

    flash('Некорректный ввод данных. Проверьте и введите заново', 'danger')
    return redirect(url_for("login_user_get"))
