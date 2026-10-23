import json

import requests
from celery import shared_task
from celery.utils.log import get_task_logger

from rest_api import models

logger = get_task_logger(__name__)


@shared_task
def post_model(data):
    model = models.FmuModel.objects.get(model_name=data["model_name"])
    url = f"http://{data['container_id']}:8000/upload/{data['model_name']}"
    logger.info("Posting model %s to %s", model.model_name, url)

    with model.epw_file.open("rb") as epw_file, model.idf_file.open("rb") as idf_file:
        files = {
            "epw": ("a.epw", epw_file, "application/octet-stream"),
            "idf": ("a.idf", idf_file, "application/octet-stream"),
            "json": (None, json.dumps(data), "application/json"),
        }
        response = requests.post(url, files=files, timeout=120)
    response.raise_for_status()
    return response.status_code


@shared_task
def post_input(data):
    url = f"http://{data['container_id']}:8000/model_input"
    logger.info("Posting time step to %s", url)
    response = requests.post(
        url,
        json={"time_step": str(data["time_step"])},
        timeout=30,
    )
    response.raise_for_status()
    return response.status_code
