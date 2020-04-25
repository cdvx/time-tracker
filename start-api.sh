#!/bin/bash

echo "<<<<<<<< create virtual env >>>>>>>>>"

# python3 -m venv

echo "<<<<<<<< source env >>>>>>>>>"
. .env

echo "<<<<<<<< install dependecies >>>>>>>>>"
# pip install -r requirements.txt


echo "<<<<<<<< run celery.sh >>>>>>>>>"
bash celery.sh &&

sleep 3
wait $BACK_PID

echo "<<<<<<<< run app >>>>>>>>>"
flask run







