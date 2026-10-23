#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

pids=()

shutdown() {
    trap - TERM INT EXIT
    if ((${#pids[@]})); then
        kill -TERM "${pids[@]}" 2>/dev/null || true
        wait "${pids[@]}" 2>/dev/null || true
    fi
}

trap shutdown TERM INT EXIT

python generator_api.py &
pids+=("$!")
celery -A generator_tasks worker --loglevel=info --concurrency=1 --queues=gen &
pids+=("$!")
python fmu_volume_monitor.py /home/fmu/code/energy/test &
pids+=("$!")

wait -n "${pids[@]}"
