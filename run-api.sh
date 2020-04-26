echo "<<<<<<<< run celery.sh >>>>>>>>>"
bash celery.sh &

sleep 3
# wait $BACK_PID

echo "<<<<<<<< run app >>>>>>>>>"
flask run 
