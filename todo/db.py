import datetime

from sqlalchemy import desc
from . import db


class User(db.Model):
    email = db.Column(db.String, unique=True)
    login = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    creating_date = db.Column(db.DateTime)

    def __init__(self, email, login, password):
        self.email = email
        self.login = login
        self.password = password
        self.creating_date = datetime.datetime.now()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120))
    done = db.Column(db.Boolean)
    date = db.Column(db.DateTime)
    user_login = db.Column(db.String, db.ForeignKey('user.login'), nullable=False)

    def __init__(self, task, login):
        self.task = task
        self.done = False
        self.date = datetime.datetime.now()
        self.user_login = login


# db.drop_all()
# db.create_all()


def add_user_to_db(user_data):
    db.session.add(user_data)
    db.session.commit()


def get_user_by_login(user_login):
    return User.query.filter_by(login=user_login).first()


def get_user_by_email(user_email):
    return User.query.filter_by(email=user_email).first()


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


def get_todo_list(user_login):
    return Todo.query.order_by(desc(Todo.date)).filter_by(user_login=user_login)
