#!/bin/bash

# shutdonw running processes if any

# bash stop-app.sh &&

# sleep 2

echo "<<<<<<<< run redis >>>>>>>>>"
bash redis.sh&

sleep 2
echo "<<<<<<<< source env >>>>>>>>>"

. .env


echo "<<<<<<<< run celery worker and celery beat >>>>>>>>>"


celery worker -A celery_worker.celery_app --loglevel=info &

celery -A tracker.celery_conf.celery_periodic_scheduler beat --loglevel=info &

echo "<<<<<<<< celery running >>>>>>>>>"

