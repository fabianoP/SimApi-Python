from celery import Celery
import requests
import time
import os.path
import json
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

rabbit_path = 'amqp://user:pass@broker:5672/vhost'
redis_path = 'redis://redis:6379/0'
app = Celery('simulator_tasks', broker=rabbit_path, backend=rabbit_path)

app.conf.task_routes = {'simulator_tasks.*': {'queue': 'sim'}}
# TODO PASS TOKEN AND SET USER FROM DJANGO
login_url = 'http://web:8000/login/'
# replace with your superuser
login_data = {"username": "user@user.com",  # username = email
              "password": "user user88"}

resp = requests.post(login_url, data=login_data)

print(resp.content)

json_resp = resp.json()

token = json_resp['token']  # get validation token
header = {'Authorization': 'Token ' + token}  # set request header


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


@app.task
def set_model(model_params):
    model_params = json.loads(model_params)
    model_name = model_params['model_name']
    step_size = model_params['step_size']
    final_time = model_params['final_time']
    fmu_path = '/home/deb/code/fmu_location/' + model_name + '/' + model_name + '.fmu'
    logger.info(f'PATH TO FMU IN SET_MODEL: {fmu_path}')
    time.sleep(5)

    params = {'model_name': model_name,
              'step_size': step_size,
              'final_time': final_time,
              'fmu_path': fmu_path}

    with open('./store_incoming_json/model_params.json', 'r') as json_file:
        data = json.load(json_file)
        logger.info(f'DATA JSON LOAD IN SET MODEL TASK {data}')

        data['model_params'].append(params)

        logger.info(f'DATA PARAMS IN SET MODEL TASK AFTER APPEND {data}')

    write_json(data, './store_incoming_json/model_params.json')


@app.task
def post_output(output_json):  # TODO refactor to send output data to api db
    logger.info(f'post_output -> output_json {output_json}')
    output_url = 'http://web:8000/output/'

    r = requests.post(output_url, headers=header, data=json.dumps(output_json))
    logger.info(f'post_output -> request status {r.status_code}')
