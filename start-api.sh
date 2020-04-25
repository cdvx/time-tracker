#!/bin/bash

echo "<<<<<<<< create virtual env >>>>>>>>>"

python3 -m venv

echo "<<<<<<<< activate env >>>>>>>>>"
. venv/bin/activate

echo "<<<<<<<< source env >>>>>>>>>"
. .env


echo "<<<<<<<< install dependecies >>>>>>>>>"
pip install -r requirements.txt


echo "<<<<<<<< run celery.sh >>>>>>>>>"
bash celery.sh &

sleep 3
# wait $BACK_PID

echo "<<<<<<<< run app >>>>>>>>>"
flask run  | tee logs/app.log | sed -e 's/^/[Command1] /'







