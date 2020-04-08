#!/bin/bash

QUEUE_NAME=$(cat /etc/hostname)

python ./simulator_api/sim_api.py \
& celery -A simulator_tasks worker -l info --concurrency=1 --queues="$QUEUE_NAME" \
& python simulation_process.py
