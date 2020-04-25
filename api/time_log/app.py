from flask import Flask, render_template, Blueprint, request, redirect, url_for
from celery import Celery
import json

from flask_cors import cross_origin

from api.storage import DataStore
from celery_conf.tasks import send_email as send_email_report


time_log = Blueprint('time_log', __name__)

store = DataStore()

@time_log.route('/', methods=['GET', 'POST'])
def home():
    data, date = store.get_data()
    if request.method == 'POST':
        request_data = request.get_json()
        email = request_data['email']
        try:
            send_email_report.delay(email, data, date)
        except Exception as e:
            print('Error occured', e)

    return render_template('table.html', data=data, date=str(date))


@time_log.route('/inspect')
def inspect():
    data = store.get_data()
    import flask
    return flask.jsonify(data)
