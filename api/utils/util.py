from datetime import datetime, timedelta, date
import json
import os
import pdfkit


class Util:

    @staticmethod
    def yesterday(in_words=False):
        yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
        if in_words:
            kwargs = {
                'year': int(yesterday[:4]),
                'month': int(yesterday[5:7]),
                'day': int(yesterday[8:10])
            }
            return date(**kwargs).strftime('%A %d %B %Y')
        return yesterday
    
    @staticmethod
    def today():
        return datetime.strftime(datetime.now(), '%Y-%m-%d')

    @staticmethod
    def start_time():
        return datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

    @staticmethod
    def format_user(user):
        return {
            'id': user['id'],
            'name': user['name'],
        }

    @staticmethod
    def open_file(file_name):
        with open(file_name) as file:
                data = json.load(file)
        return data

    @staticmethod
    def write_to_file(data, file_name):
        with open(os.path.join(os.path.dirname(__file__), '../', 'storage', file_name), 'w') as file:
            json.dump(data, file)

    # @staticmethod
    # def download_report():
    #     config = pdfkit.configuration(wkhtmltopdf="path_to_exe")
    #     pdfkit.from_url(
    #         'http://localhost:5000/',
    #         os.path.join(os.path.dirname(__file__), f'../../{Util.yesterday()}.pdf'),
    #         configuration = config)
