from __future__ import absolute_import

from celery import shared_task

#app = Celery('tasks', broker='redis://localhost:6379/0')

@shared_task
def add(x, y):
    return x+y
