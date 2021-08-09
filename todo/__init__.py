import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

try:
    os.environ['DATABASE_URL'] is None
except KeyError:
    os.environ['DATABASE_URL'] = 'sqlite:////tmp/todo.db'

app = Flask(__name__)
if 'postgres' in os.environ['DATABASE_URL']:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace('postgres', 'postgresql')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)

from . import routes
