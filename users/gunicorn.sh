#!/bin/bash
set -e

echo "Starting SSH ...."
service ssh start

gunicorn --chdir app app:app -w 2 --threads 2 -b 0.0.0.0:5000 --error-logfile ../app-error-log
