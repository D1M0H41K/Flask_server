import logging
import os
import time

from celery import Celery

from . import app
from .db import integrate_todo_db

logger = logging.getLogger(__name__)


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
    logger.info("Log example: Received todo: %d, Going to sleep for %d seconds", todo_id, sleep_time)
    time.sleep(sleep_time)
    logger.info("Log example: Back from the sleep for todo: %d, integrating!", todo_id)
    integrate_todo_db(todo_id=todo_id)
