import json
import os
import requests

from celery_conf.celery_periodic_scheduler import celery_scheduler 
from config import AppConfig
from api.utils import Util

from flask import render_template
from flask_mail import Message
from main import mail

headers = {
    "App-Token": AppConfig.APP_TOKEN,
    "Auth-Token": AppConfig.AUTH_TOKEN
}

@celery_scheduler.task(name='get_daily_logged_time')
def get_daily_logged_time():
    API_URL = os.getenv('API_V1')

    data= requests.get(API_URL, headers=headers)
    data = data.json()

    Util.write_to_file(data, os.getenv('ORGANIZATIONS'))

    get_daily_projects.delay()
    get_daily_activity.delay()

@celery_scheduler.task(name='get_daily_projects')
def get_daily_projects():
    API_URL = os.getenv('API_PROJECTS')

    data= requests.get(API_URL, headers=headers)
    data = data.json()

    Util.write_to_file(data, os.getenv('PROJECTS'))

@celery_scheduler.task(name='get_daily_project_activity')
def get_daily_activity():
    API_URL = os.getenv('API_ACTIVITIES')

    start_time = str(Util.start_time())
    stop_time = str(Util.today())

    data= requests.get(f'{API_URL}?start_time={start_time}&stop_time={stop_time}', headers=headers)
    data = data.json()

    Util.write_to_file(data, os.getenv('ACTIVITIES'))

@celery_scheduler.task(name='reset_logs')
def reset_logs():
    Util.rest_logs()

@celery_scheduler.task(name='send_email')
def send_email(email, data, date):
    msg = Message("Time log report",
                  recipients=[email])
    msg.html = render_template('table.html', data=data, date=str(date))
    mail.send(msg)

