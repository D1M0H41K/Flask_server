import os

from json import JSONEncoder, JSONDecoder
import datetime


data_path = "data"
data_file = "todo_list.json"


class Todo:
    _id = 1

    def __init__(self, task, done=False, date=None, task_id=0):
        self.task = task
        self.done = done
        self.date = date if date else datetime.datetime.now()
        self.id = task_id if task_id else Todo._id
        Todo._id += self.id + 1


class JsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return str(o.isoformat())
        else:
            return o.__dict__


def from_json(json_object):
    try:
        return Todo(json_object['task'],
                    json_object['done'],
                    datetime.datetime.fromisoformat(json_object['date']),
                    json_object['id'])
    except KeyError and ValueError:
        return


def read_json():
    try:
        with open(os.path.join(data_path, data_file), 'r') as read_file:
            todo_list = []
            data = read_file.read()
        if data:
            todo_list = JSONDecoder(object_hook=from_json).decode(data)
        return todo_list
    except FileNotFoundError:
        return []


def write_json(todo_list):
    try:
        with open(os.path.join(data_path, data_file), 'w+') as out_file:
            out_file.write(JsonEncoder().encode(todo_list))
    except FileNotFoundError:
        os.mkdir(data_path)
        write_json(todo_list)
