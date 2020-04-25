from flask import Flask, render_template, Blueprint
from celery import Celery
import json

from api.storage import DataStore

time_log = Blueprint('time_log', __name__)

store = DataStore()

@time_log.route('/')
def home():
    data, date = store.get_data()
    from api.utils import Util
    # 
    return render_template('table.html', data=data, date=str(date))

@time_log.route('/inspect')
def inspect():
    data = store.get_data()
    import flask
    from api.utils import Util
    # Util.download_report()
    return flask.jsonify(data)
