#!/bin/bash

echo "<<<<<<<< stop celery >>>>>>>>>"

ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9 &

echo "<<<<<<<< stopped worker >>>>>>>>>" 
ps auxww | grep 'celery beat' | awk '{print $2}' | xargs kill -9 &
echo "<<<<<<<< stopped beat >>>>>>>>>"
ps auxww | grep 'celery' | awk '{print $2}' | xargs kill -9 &

rm celerybeat.pid &

echo "<<<<<<<< celery down >>>>>>>>>"

echo "<<<<<<<< stop redis >>>>>>>>>"

redis-cli shutdown &

echo "<<<<<<<< redis down >>>>>>>>>"

echo "<<<<<<<< stop flask >>>>>>>>>"

ps auxww | grep 'flask' | awk '{print $2}' | xargs kill -9

echo "<<<<<<<< flask down >>>>>>>>>"
