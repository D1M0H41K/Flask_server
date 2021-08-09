from app import db
import datetime


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120))
    done = db.Column(db.Boolean)
    date = db.Column(db.DateTime)

    def __init__(self, task):
        self.task = task
        self.done = False
        self.date = datetime.datetime.now()


db.create_all()


def add_todo_to_db(todo_task):
    db.session.add(todo_task)
    db.session.commit()


def get_todo_by_id(todo_id):
    return Todo.query.filter_by(id=todo_id).first()


def commit_db_changes():
    db.session.commit()


def remove_todo_by_id(todo_id):
    db.session.delete(get_todo_by_id(todo_id))
    db.session.commit()


def get_todo_list():
    return Todo.query.all()
