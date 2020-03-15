from celery import Celery, Task
import requests
import time
import os.path
import json
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from simulator.simulation_obj import SimulationObject
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

rabbit_path = 'amqp://user:pass@broker:5672/vhost'
redis_path = 'redis://redis:6379/0'
app = Celery('simulator_tasks', broker=rabbit_path, backend=rabbit_path)

app.conf.task_routes = {'simulator_tasks.*': {'queue': 'sim'}}

login_url = 'http://web:8000/login/'
# replace with your superuser
login_data = {"username": "test@test.com",  # username = email
        "password": "test user88"}

resp = requests.post(login_url, data=login_data)

print(resp.content)

json_resp = resp.json()

token = json_resp['token']  # get validation token
header = {'Authorization':  'Token ' + token}  # set request header


def write_json(data, filename):
    with open(filename, 'a+') as f:
        json.dump(data, f, indent=4)


class ModelInitTask(Task):
    _model = None

    def run(self, *args, **kwargs):
        pass

    def model_get(self):
        return self._model

    def model_setter(self, model):
        if self._model is None:
            self._model = model


model_instance = ModelInitTask()


@app.task
def set_model(model_params):
    model_params = json.loads(model_params)
    model_name = model_params['model_name']
    step_size = model_params['step_size']
    final_time = model_params['final_time']
    fmu_path = '/home/deb/code/fmu_location/' + model_name + '/' + model_name + '.fmu'
    logger.info(f'PATH TO FMU IN SET_MODEL: {fmu_path}')
    time.sleep(10)
    model = SimulationObject(model_name=model_name, step_size=int(step_size),
                             final_time=float(final_time),
                             path_to_fmu=fmu_path)

    model.model_init()
    model_instance.model_setter(model=model)


@app.task
def model_input(input_json):
    logger.info(f'model_input -> input_json {input_json}')
    output_data = model_instance.model.do_time_step(input_json)
    # TODO write output to .json, move below to monitor
    with open('/home/deb/code/store_outgoing_json/outputs.json') as json_file:
        data = json.load(json_file)

        temp = data['outputs']

        temp.append(output_data)

    write_json(data, '/home/deb/code/store_outgoing_json/outputs.json')
