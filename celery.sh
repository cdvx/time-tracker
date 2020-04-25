#!/bin/bash
echo "<<<<<<<< run redis >>>>>>>>>"
bash redis.sh | tee logs/redis.log | sed -e 's/^/[Command1] /' &

sleep 2
echo "<<<<<<<< source env >>>>>>>>>"

. .env

rm -rf celerybeat.pid &&

ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9 &

sleep 2

ps auxww | grep 'celery worker' | awk '{print $2}' &

echo "<<<<<<<< run celery worker and celery beat >>>>>>>>>"


celery worker -A celery_worker.celery_app --loglevel=info | tee logs/celery-worker.log | sed -e 's/^/[Command1] /' &

celery -A celery_conf.celery_periodic_scheduler beat --loglevel=info | tee logs/celery-beat.log | sed -e 's/^/[Command1] /' &

echo "<<<<<<<< celery running >>>>>>>>>"

