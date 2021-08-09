from flask import request, render_template, redirect

from . import app
from .db import Todo, remove_todo_by_id, add_todo_to_db, get_todo_by_id, \
    commit_db_changes, get_todo_list


def remove_todo_db(todo_id):
    remove_todo_by_id(todo_id)


def add_todo_db(data):
    if 'task' in data and data.get('task') != '':
        add_todo_to_db(Todo(data.get('task')))


def update_todo_db(data, todo_id):
    todo_task = get_todo_by_id(todo_id)
    if 'done' in data:
        todo_task.done = not todo_task.done
    commit_db_changes()


@app.route('/')
def hello_world():
    return redirect('/todo')


@app.route('/todo', methods=['GET', 'POST'])
def todo_main():
    if request.method == 'POST':
        add_todo_db(request.form)
        return redirect('/todo')
    else:
        todo_list = get_todo_list()
        return render_template('todo.html', todo_list=sorted(todo_list, key=lambda todo: todo.date, reverse=True))


@app.route('/todo/<todo_id>/update', methods=['POST'])
def todo_update(todo_id=None):
    update_todo_db(request.form, int(todo_id))
    return redirect('/todo')


@app.route('/todo/<todo_id>/delete', methods=['POST'])
def todo_remove(todo_id=None):
    remove_todo_db(int(todo_id))
    return redirect('/todo')
