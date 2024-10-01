#!/bin/bash

PORT=8002

if lsof -i :$PORT > /dev/null; then
    echo "Port $PORT is already in use. Killing all processes using the port"
    lsof -t -i :$PORT | xargs -r kill -9
    sleep 2
fi

exec /home/ubuntu/.cache/pypoetry/virtualenvs/poetry_install-L0t7h3YQ-py3.12/bin/gunicorn --workers 3 --bind 0.0.0.0:8002 -c /home/ubuntu/test_task2/deployment_configs/gunicorn.conf.py -k uvicorn.workers.UvicornWorker main:app
