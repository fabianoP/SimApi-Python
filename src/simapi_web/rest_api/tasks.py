from celery import shared_task
from celery.utils.log import get_task_logger
import requests
import json

from rest_api import models

logger = get_task_logger(__name__)


@shared_task
def post_model(data):
    logger.info(f'post_model data {data}')
    auth_t = data['Authorization']
    logger.info(f'post_model data AUTH {auth_t}')
    model = models.FmuModelParameters.objects.get(model_name=data['model_name'])

    # TODO set simulator generic for multiple containers
    if model is not None:

        url = 'http://simulator:8000/upload/' + data['model_name']

        file = {'epw':  ('a.epw', open(model.epw_file.path, 'rb'), 'application/octet-stream'),
                'idf':  ('a.idf', open(model.idf_file.path, 'rb'), 'application/octet-stream'),
                'json': (None, json.dumps(data), 'application/json')}

        r = requests.post(url, files=file)

        return r.status_code


@shared_task
def post_input(data):
    logger.info(f'post_input data {data}')
    # TODO create middleware to add DateTime to data
    input_instance = models.Input.objects.last()

    if input_instance is not None:
        url = 'http://simulator:8000/model_input'

        headers = {'Content-type': 'application/json'}

        r = requests.post(url=url, json=data, headers=headers)
