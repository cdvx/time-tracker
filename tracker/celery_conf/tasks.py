"""Module for celery tasks"""

# system libraries
import json
import os

# 3rd party libraries
import requests
from flask import render_template
from flask_mail import Message

# local imports
from config import AppConfig
from main import mail
from tracker.celery_conf.celery_periodic_scheduler import celery_scheduler
from tracker.utils import Util

# required headers for Hubstaff API
headers = {
    "App-Token": AppConfig.APP_TOKEN,
    "Auth-Token": AppConfig.AUTH_TOKEN
}


@celery_scheduler.task(name='get_daily_logged_time')
def get_daily_logged_time():
    """
    Get daily time log data from API and write it to a file
    Call other methods to get relevant data

    Returns:
        None
    """
    API_URL = os.getenv('API_V1')

    data= requests.get(API_URL, headers=headers)
    data = data.json()

    Util.write_to_file(data, os.getenv('ORGANIZATIONS'))

    get_daily_projects.delay()
    get_daily_activity.delay()

@celery_scheduler.task(name='get_daily_projects')
def get_daily_projects():
    """
    Get daily projects activity data from API and write it to a file

    Returns:
        None
    """
    API_URL = os.getenv('API_PROJECTS')

    data= requests.get(API_URL, headers=headers)
    data = data.json()

    Util.write_to_file(data, os.getenv('PROJECTS'))

@celery_scheduler.task(name='get_daily_project_activity')
def get_daily_activity():
    """
    Get daily activities data from API and write it to a file

    Returns:
        None
    """
    API_URL = os.getenv('API_ACTIVITIES')

    start_time = str(Util.start_time())
    stop_time = str(Util.yesterday())

    data= requests.get(f'{API_URL}?start_time={start_time}&stop_time={stop_time}', headers=headers)
    data = data.json()

    Util.write_to_file(data, os.getenv('ACTIVITIES'))


@celery_scheduler.task(name='send_email')
def send_email(email, data, date):
    """
    Send email report

    Args:
        email(str): email to send report to
        data(list): list of organisation objects/dicts
        date(date): date object of the report date

    Returns:
        None
    """
    msg = Message("Time log report",
                  recipients=[email])
    msg.html = render_template('table.html', data=data, date=str(date))
    mail.send(msg)
