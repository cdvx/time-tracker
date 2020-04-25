#!/bin/bash

echo "<<<<<<<< stop celery >>>>>>>>>"
ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9 
ps auxww | grep 'celery' | awk '{print $2}' | xargs kill -9 

echo "<<<<<<<< celery down >>>>>>>>>"

echo "<<<<<<<< stop redis >>>>>>>>>"

ps auxww | grep 'redis' | awk '{print $2}' | xargs kill -9

echo "<<<<<<<< redis down >>>>>>>>>"

echo "<<<<<<<< stop flask redis >>>>>>>>>"

ps auxww | grep 'flask' | awk '{print $2}' | xargs kill -9

echo "<<<<<<<< flask down >>>>>>>>>"
