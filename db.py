from json import JSONEncoder, JSONDecoder
import datetime


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


def read_json():
    with open('data/todo_list.json', 'r') as read_file:
        todo_list = []
        data = read_file.read()
        if data:
            todo_list = JSONDecoder(object_hook=from_json).decode(data)
        return todo_list


def write_json(todo_list):
    with open('data/todo_list.json', 'w') as out_file:
        out_file.write(JsonEncoder().encode(todo_list))
