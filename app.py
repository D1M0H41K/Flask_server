from flask import Flask, request, render_template, redirect
from db import read_json, write_json, Todo

app = Flask(__name__)


def remove_todo(data, todo_id, todo_list):
    for todo_task in todo_list:
        if todo_task.id == todo_id:
            todo_list.remove(todo_task)
            break
    write_json(todo_list)


def update_todo(data, todo_id, todo_list):
    if 'done' in data:
        for todo_task in todo_list:
            if todo_task.id == todo_id:
                todo_task.done = not todo_task.done
                break
    write_json(todo_list)


def add_todo(data, todo_list):
    if 'task' in data and data.get('task') != '':
        todo_list.append(Todo(data.get('task')))
        write_json(todo_list)


@app.route('/')
def hello_world():
    return redirect('/todo')


@app.route('/todo', methods=['GET', 'POST'])
def todo_main():
    todo_list = read_json()
    if request.method == 'POST':
        add_todo(request.form, todo_list)
        return redirect('/todo')
    else:
        return render_template('todo.html', todo_list=sorted(todo_list, key=lambda todo: todo.date, reverse=True))


@app.route('/todo/<todo_id>/update', methods=['POST'])
def todo_update(todo_id=None):
    todo_list = read_json()
    update_todo(request.form, int(todo_id), todo_list)
    return redirect('/todo')


@app.route('/todo/<todo_id>/delete', methods=['POST'])
def todo_remove(todo_id=None):
    todo_list = read_json()
    remove_todo(request.form, int(todo_id), todo_list)
    return redirect('/todo')


if __name__ == '__main__':
    app.run()

