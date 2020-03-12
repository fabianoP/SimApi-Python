from celery import Celery
import os.path
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from energy_plus_to_fmu import RunEnergyPlusToFMU

rabbit_path = 'amqp://user:pass@broker:5672/vhost'
redis_path = 'redis://redis:6379/0'
app = Celery('generator_tasks', broker=rabbit_path, backend=rabbit_path)
app.conf.task_routes = {'generator_tasks': {'queue': 'gen'}}


@app.task(bind=True)
def gen_fmu(idf, epw, directory):
    energy_plus = RunEnergyPlusToFMU(idf=idf, epw=epw, directory=directory)
    energy_plus.run()
