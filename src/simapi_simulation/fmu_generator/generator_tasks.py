from celery import Celery
import os.path
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from energy_plus_to_fmu import RunEnergyPlusToFMU

rabbit_path = 'amqp://user:pass@broker:5672/vhost'
backend = 'db+postgresql://postgres:backend@backend/backend_db'
app = Celery('generator_tasks', broker=rabbit_path, backend=backend)

app.conf.task_routes = {'generator_tasks.*': {'queue': 'gen'}}


@app.task
def gen_fmu(idf, epw, directory):
    energy_plus = RunEnergyPlusToFMU(idf=idf, epw=epw, directory=directory)
    result = energy_plus.run()

    return result
