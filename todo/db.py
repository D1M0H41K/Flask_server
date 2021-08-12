import os
from collections import defaultdict

from sqlalchemy import func, desc
from flask_login import UserMixin
from wtforms import Form, StringField, validators, PasswordField
from . import db, login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    creating_date = db.Column(db.DateTime, server_default=func.now())
    todos = db.relationship("Todo", order_by="desc(Todo.date)", backref='user')
    integrating_list = defaultdict(object)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


class RegistrationForm(Form):
    email = StringField(label="Email:", validators=[validators.Length(min=5, max=90), validators.DataRequired()])
    login = StringField(label="Login:", validators=[validators.Length(min=4, max=32), validators.DataRequired()])
    password = PasswordField(label="Password:", validators=[validators.DataRequired()])


class LogInForm(Form):
    login = StringField(label="Login:", validators=[validators.DataRequired()])
    password = PasswordField(label="Password:", validators=[validators.DataRequired()])


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120), nullable=False)
    done = db.Column(db.Boolean, server_default='0')
    date = db.Column(db.DateTime, server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    integrated = db.Column(db.Boolean, default=False)


if 'DROP_TABLES' in os.environ:
    db.drop_all()
    db.create_all()


if not db.engine.table_names():
    db.create_all()


def add_user_to_db(user_data):
    db.session.add(user_data)
    db.session.commit()


def get_user_by_login(user_login):
    return User.query.filter_by(login=user_login).first()


def get_user_by_email(user_email):
    return User.query.filter_by(email=user_email).first()


def add_todo_to_db(todo_task, user):
    user.todos.append(todo_task)
    db.session.commit()


def get_todo_by_id(todo_id):
    return Todo.query.get(todo_id)


def commit_db_changes():
    db.session.commit()


def remove_todo_by_id(todo_id):
    db.session.delete(get_todo_by_id(todo_id))
    db.session.commit()


def get_todo_list(user):
    return user.todos
