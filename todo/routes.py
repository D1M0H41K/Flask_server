import os

from flask import request, render_template, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user
from . import app, login_manager
from .db import Todo, remove_todo_by_id, add_todo_to_db, get_todo_by_id, \
    commit_db_changes, get_todo_list, User, add_user_to_db, get_user_by_login, \
    get_user_by_email, RegistrationForm, LogInForm


def remove_todo_db(todo_id):
    remove_todo_by_id(todo_id)


def add_todo_db(data):
    if 'task' in data and data.get('task') != '':
        add_todo_to_db(Todo(task=data.get('task'), user_id=session['_user_id']))


def update_todo_db(data, todo_id):
    todo_task = get_todo_by_id(todo_id)
    if 'done' in data:
        todo_task.done = not todo_task.done
    commit_db_changes()


def get_user_data(data):
    if get_user_by_login(data.login.data) is not None:
        if check_password_hash(pwhash=get_user_by_login(data.login.data).password, password=data.password.data):
            return get_user_by_login(data.login.data)
    elif get_user_by_email(data.login.data) is not None:  # Here login is email
        if check_password_hash(pwhash=get_user_by_email(data.login.data).password, password=data.password.data):
            return get_user_by_email(data.login.data)
    flash('Not correct login or password')


def register_user(data):
    if get_user_by_login(data.login.data) is None:
        if get_user_by_email(data.email.data) is None:
            add_user_to_db(User(email=data.email.data,
                                login=data.login.data,
                                password=generate_password_hash(password=data.password.data,
                                                                method=os.environ['HASH_METHOD'],
                                                                salt_length=int(os.environ['SALT_LENGTH']))))
        else:
            return flash('Account with given email already exists')
    else:
        return flash('Account with given login already exists')


@app.route('/')
def hello_world():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login_main():
    form = LogInForm(request.form)
    if request.method == 'POST':
        if form.validate():
            session['user_data'] = get_user_data(form)
        else:
            flash('Not correct data in fields')
        if '_flashes' in session:
            return redirect('/login')
        login_user(session['user_data'], remember=True)
        return redirect('/todo')
    else:
        return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_main():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate():
            register_user(form)
        else:
            flash('Not correct data in fields')
        if '_flashes' in session:
            return redirect('/register')
        return redirect('/login')
    else:
        return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')


@app.route('/todo', methods=['GET', 'POST'])
@login_required
def todo_main():
    if '_user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        add_todo_db(request.form)
        return redirect('/todo')
    else:
        todo_list = get_todo_list(session['_user_id'])
        return render_template('todo.html', todo_list=todo_list)


@app.route('/todo/<todo_id>/update', methods=['POST'])
@login_required
def todo_update(todo_id=None):
    update_todo_db(request.form, int(todo_id))
    return redirect('/todo')


@app.route('/todo/<todo_id>/delete', methods=['POST'])
@login_required
def todo_remove(todo_id=None):
    remove_todo_db(int(todo_id))
    return redirect('/todo')
