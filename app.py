import time
from flask import Flask, request, render_template

app = Flask(__name__)


class todo_object:
    _id = 0

    def __init__(self, task):
        self.task = task
        self.done = False
        self.date = time.asctime(time.localtime())
        self.id = todo_object._id
        todo_object._id += 1


todo_list = [todo_object("Buy eggs"), todo_object("Bake bread")]


def update_todo_list(data):
    if 'task' in data:
        todo_list.append(todo_object(data.get('task')))
    elif 'id' in data:
        if 'done' in data:
            todo_list[int(data.get('id'))].done = True
        else:
            todo_list[int(data.get('id'))].done = False


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/todo', methods=['GET', 'POST'])
def todo_main():
    if request.method == 'POST':
        update_todo_list(request.form)
        return render_template('todo.html', todo_list=sorted(todo_list, key=lambda todo: todo.date, reverse=True))
    else:
        return render_template('todo.html', todo_list=todo_list)


if __name__ == '__main__':
    app.run()

