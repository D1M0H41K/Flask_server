from flask import Flask, request, render_template, redirect
from db import read_json, write_json, Todo

app = Flask(__name__)


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
        write_json(todo_list)


@app.route('/')
def hello_world():
    return redirect('/todo')


@app.route('/todo', methods=['GET', 'POST'])
def todo_main():
    todo_list = read_json()
    if request.method == 'POST':
        update_todo_list(request.form, todo_list)
        return redirect('/todo')
    else:
        return render_template('todo.html',
                               todo_list=sorted(todo_list, key=lambda todo: todo.date, reverse=True))


if __name__ == '__main__':
    app.run()

