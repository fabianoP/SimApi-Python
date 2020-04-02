#!/bin/bash

QUEUE_NAME=$(cat /etc/hostname)

python post_hostname.py

python ./simulator_api/sim_api.py \
& python volume_monitor.py /home/deb/code/volume \
& celery -A simulator_tasks worker -l info --concurrency=1 --queues="$QUEUE_NAME" \
& python fmu_location_monitor.py /home/deb/code/fmu_location \
& python simulation_process.py