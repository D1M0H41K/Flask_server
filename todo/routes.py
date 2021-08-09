import os

from flask import request, render_template, redirect, session

from . import app
from .db import Todo, remove_todo_by_id, add_todo_to_db, get_todo_by_id, \
    commit_db_changes, get_todo_list


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
    if 'email' in data:
        return data.get('email')


@app.route('/')
def hello_world():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login_main():
    app.config['SECRET_KEY'] = os.urandom(16)
    if request.method == 'POST':
        session['user_data'] = get_user_data(request.form)
        if session['user_data']:
            return redirect('/todo')
    else:
        return render_template('login.html')


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
