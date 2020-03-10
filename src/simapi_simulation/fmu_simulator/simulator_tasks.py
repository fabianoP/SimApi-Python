from celery import Celery
import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from simulator import simulation_obj

rabbit_path = 'amqp://user:pass@broker:5672/vhost'
redis_path = 'redis://redis:6379/0'
app = Celery('tasks', broker=rabbit_path, backend=rabbit_path)


