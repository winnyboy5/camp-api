#!/bin/sh
gunicorn --chdir app app:app -w 2 --threads 2 -b 0.0.0.0:5002 --error-logfile ../app-error-log
