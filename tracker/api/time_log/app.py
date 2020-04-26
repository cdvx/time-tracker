"""Module for time log endpoints"""

# system libraries
import json

# 3rd party libraries
from celery import Celery
from flask import (Blueprint, Flask, jsonify, redirect, render_template,
                   request, url_for)
from flask_cors import cross_origin

# local imports
from tracker.celery_conf.tasks import send_email as send_email_report
from tracker.storage import DataStore

time_log = Blueprint('time_log', __name__)

store = DataStore()

@time_log.route('/', methods=['GET', 'POST'])
def home():
    """
    Render html showing timelogged for the previous
    day.
    Args:
        None:
    Returns:
        render_template: html template renderred with required data
    """

    data, date = store.get_data()

    # user has posted email
    if request.method == 'POST':
        request_data = request.get_json()
        email = request_data['email']
        try:
            send_email_report.delay(email, data, date)
            return render_template('table.html', data=data, date=str(date))
        except Exception as e:
            print('Error occured', e)

    return render_template('table.html', data=data, date=str(date))


@time_log.route('/inspect')
def inspect():
    """
    Return JSON data used by the home endpoint
    Args:
        None:
    Returns:
        Response: JSON response of the data.
    """
    data = store.get_data()
    return jsonify(data)
