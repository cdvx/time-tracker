#!/bin/bash
echo "<<<<<<<< sun redis >>>>>>>>>"
bash redis.sh &

sleep 2
echo "<<<<<<<< source env >>>>>>>>>"

. .env

ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9 &

sleep 2

ps auxww | grep 'celery worker' | awk '{print $2}' 

echo "<<<<<<<< run celery worker and celery beat >>>>>>>>>"


celery worker -A celery_worker.celery_app --loglevel=info &
celery -A celery_conf.celery_periodic_scheduler beat --loglevel=info &

echo "<<<<<<<< celery running >>>>>>>>>"
