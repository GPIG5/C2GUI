from __future__ import absolute_import

from celery import shared_task

import socket

#app = Celery('tasks', broker='redis://localhost:6379/0')

@shared_task
def add(x, y):
    return x+y

@shared_task
def send_search_area_coord(coords):
    s = socket.socket()
    host = socket.gethostname()
    return host
