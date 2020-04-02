#!/bin/bash

python generator_api.py \
& celery -A generator_tasks worker -l info --concurrency=1 --queues=gen \
& python fmu_volume_monitor.py /home/fmu/code/energy/test