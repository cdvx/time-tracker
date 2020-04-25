echo "<<<<<<<< run celery.sh >>>>>>>>>"
bash celery.sh &

sleep 3
# wait $BACK_PID

echo "<<<<<<<< run app >>>>>>>>>"
flask run  | tee logs/app.log | sed -e 's/^/[Command1] /'
