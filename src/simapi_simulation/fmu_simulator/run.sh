#!/usr/bin/env bash

set -Eeuo pipefail

QUEUE_NAME=$(cat /etc/hostname)
pids=()

terminate() {
    trap - EXIT INT TERM
    if ((${#pids[@]})); then
        kill "${pids[@]}" 2>/dev/null || true
        wait "${pids[@]}" 2>/dev/null || true
    fi
}

trap terminate EXIT INT TERM

python ./simulator_api/sim_api.py &
pids+=("$!")
python volume_monitor.py /home/deb/code/volume &
pids+=("$!")
celery -A simulator_tasks worker -l info --concurrency=1 --queues="$QUEUE_NAME" &
pids+=("$!")
python fmu_location_monitor.py /home/deb/code/fmu_location &
pids+=("$!")
python simulation_process.py &
pids+=("$!")

wait -n "${pids[@]}"
