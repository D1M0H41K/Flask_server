import os

from celery import Celery
from .db import integrate_todo_db
from . import app

import time


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app.config.update(
    CELERY_BROKER_URL=os.environ['CELERY_BROKER_URL']
)
celery = make_celery(app)


@celery.task()
def integrate(sleep_time, todo_id):
    time.sleep(sleep_time)
    integrate_todo_db(todo_id=todo_id)

