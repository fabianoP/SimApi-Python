from celery import shared_task
from rest_api import models
from celery.utils.log import get_task_logger
import requests
import json

logger = get_task_logger(__name__)

# TODO Major problem with workers receiving wrong jobs. Need separation


@shared_task(bind=True)
def post_model(data):
    logger.info(f'post_model data {data}')
    model = models.FmuModelParameters.objects.get(model_name=data['model_name'])

    # TODO set simulator generic for multiple containers
    if model is not None:

        url = 'http://simulator:8000/upload/' + data['model_name']

        file = {'epw': ('a.epw', open(model.epw_file.path, 'rb')),
                'idf': ('a.idf', open(model.idf_file.path, 'rb'))}

        r = requests.post(url, files=file)

        if r.status_code == 200:
            url = 'http://simulator:8000/set_model'

            f_time = data['final_time']
            print(type(f_time))

            headers = {'Content-type': 'application/json'}

            r = requests.post(url=url, json=json.dumps(data), headers=headers)


@shared_task(bind=True)
def post_input(data):
    logger.info(f'post_input data {data}')
    # TODO create middleware to add DateTime to data
    input_instance = models.Input.objects.last()

    if input_instance is not None:
        url = 'http://simulator:8000/model_input'

        headers = {'Content-type': 'application/json'}

        r = requests.post(url=url, json=json.dumps(data), headers=headers)
