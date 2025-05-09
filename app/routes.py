from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash
import re

main = Blueprint('main', __name__)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        # Базовая валидация на пустые поля
        if not username or not email or not password:
            flash('Все поля обязательны')
            return redirect(url_for('main.register'))

        # Проверка длины пароля
        if len(password) < 6:
            flash('Пароль должен содержать минимум 6 символов')
            return redirect(url_for('main.register'))

        # Примитивная проверка email
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            flash('Некорректный email')
            return redirect(url_for('main.register'))

        # Проверка на дубликат username или email
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            flash('Пользователь с таким именем или email уже существует')
            return redirect(url_for('main.register'))

        # Хешируем пароль и сохраняем пользователя
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Регистрация прошла успешно!')
        return redirect(url_for('main.register'))

    return render_template('register.html')

@main.route('/user')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)