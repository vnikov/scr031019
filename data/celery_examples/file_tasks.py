import os
import time

from celery import Celery

app = Celery('tasks', backend='rpc://', broker='amqp://guest@localhost')

@app.task
def write_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

@app.task
def read_file(filename):
    while not os.path.exists(filename):
        time.sleep(1)
    with open(filename) as f:
        data = f.read()
    os.remove(filename)
    return data
