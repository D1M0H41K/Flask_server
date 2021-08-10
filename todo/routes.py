from flask import request, render_template, redirect, session, flash

from . import app
from .db import Todo, remove_todo_by_id, add_todo_to_db, get_todo_by_id, \
    commit_db_changes, get_todo_list, User, add_user_to_db, get_user_by_login, \
    get_user_by_email


def remove_todo_db(todo_id):
    remove_todo_by_id(todo_id)


def add_todo_db(data):
    if 'task' in data and data.get('task') != '':
        add_todo_to_db(Todo(data.get('task'), session['user_data']))


def update_todo_db(data, todo_id):
    todo_task = get_todo_by_id(todo_id)
    if 'done' in data:
        todo_task.done = not todo_task.done
    commit_db_changes()


def get_user_data(data):
    if 'login' in data and 'password' in data:
        if get_user_by_login(data.get('login')) is not None:
            if get_user_by_login(data.get('login')).password == data.get('password'):
                return data.get('login')
        elif get_user_by_email(data.get('login')) is not None:  # Here login is email
            if get_user_by_email(data.get('login')).password == data.get('password'):
                return get_user_by_email(data.get('login')).login
        return flash('Not correct login or password')
    return flash('Not all text fields are filled in')


def register_user(data):
    if 'login' in data and 'password' in data and 'email' in data \
            and data.get('login') != '' and data.get('password') != '' and data.get('email') != '':
        if get_user_by_login(data.get('login')) is None:
            if get_user_by_email(data.get('email')) is None:
                add_user_to_db(User(data.get('email'), data.get('login'), data.get('password')))
            else:
                return flash('Account with given email already exists')
        else:
            return flash('Account with given login already exists')
    else:
        return flash('Not all text fields are filled in')


@app.route('/')
def hello_world():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login_main():
    if request.method == 'POST':
        session['user_data'] = get_user_data(request.form)
        if '_flashes' in session:
            return redirect('/login')
        return redirect('/todo')
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_main():
    if request.method == 'POST':
        register_user(request.form)
        if '_flashes' in session:
            return redirect('/register')
        return redirect('/login')
    else:
        return render_template('register.html')


@app.route('/todo', methods=['GET', 'POST'])
def todo_main():
    if 'user_data' not in session:
        return redirect('/login')
    if request.method == 'POST':
        add_todo_db(request.form)
        return redirect('/todo')
    else:
        todo_list = get_todo_list(session['user_data'])
        return render_template('todo.html', todo_list=todo_list)


@app.route('/todo/<todo_id>/update', methods=['POST'])
def todo_update(todo_id=None):
    update_todo_db(request.form, int(todo_id))
    return redirect('/todo')


@app.route('/todo/<todo_id>/delete', methods=['POST'])
def todo_remove(todo_id=None):
    remove_todo_db(int(todo_id))
    return redirect('/todo')
