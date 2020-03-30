#!/bin/bash

python ./simulator_api/sim_api.py \
& python volume_monitor.py /home/deb/code/volume \
& celery -A simulator_tasks worker -l info --queues=sim \
& python fmu_location_monitor.py /home/deb/code/fmu_location