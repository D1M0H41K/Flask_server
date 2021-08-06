import datetime

from flask import Flask, request, render_template, redirect
from json import JSONEncoder, JSONDecoder

app = Flask(__name__)


class Todo:
    _id = 0

    def __init__(self, task, done=False, date=datetime.datetime.now(), task_id=0):
        self.task = task
        self.done = done
        self.date = date
        self.id = task_id if task_id else Todo._id
        Todo._id = task_id + 1


class JsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return str(o)
        else:
            return o.__dict__


def from_json(json_object):
    try:
        return Todo(json_object['task'],
                    json_object['done'],
                    json_object['date'],
                    json_object['id'])
    except KeyError:
        return


def update_todo_list(data, todo_list):
    try:
        if 'task' in data and data.get('task') != '':
            todo_list.append(Todo(data.get('task')))
        elif 'id' in data and data.get('id') != '':
            done = False
            if 'done' in data:
                done = True
            for todo_task in todo_list:
                if todo_task.id == int(data.get('id')):
                    todo_task.done = done
                    break
    except ValueError:
        return
    finally:
        with open('data/todo_list.json', 'w') as out_file:
            out_file.write(JsonEncoder().encode(todo_list))


@app.route('/')
def hello_world():
    return redirect('/todo')


@app.route('/todo', methods=['GET', 'POST'])
def todo_main():
    with open('data/todo_list.json', 'r') as read_file:
        todo_list = []
        data = read_file.read()
        if data:
            todo_list = JSONDecoder(object_hook=from_json).decode(data)
    if request.method == 'POST':
        update_todo_list(request.form, todo_list)
        return redirect('/todo')
    else:
        return render_template('todo.html',
                               todo_list=sorted(todo_list, key=lambda todo: todo.date, reverse=True))


if __name__ == '__main__':
    app.run()

