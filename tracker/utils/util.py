"""Module for Utility class"""

# system libraries
import json
import os
from datetime import date, datetime, timedelta


class Util:
    """Utility class with helper functions"""

    @staticmethod
    def yesterday(in_words=False, obj=False):
        """
        Get yesterday's date

        Args:
            in_words(bool): return date in words if True else
                            date object
            obj(bool): return datetime obj if False

        Returns:
            str: datetime str if obj is Truw
            str: date str if in_words is True
            datetime: return datetime object if obj is True

        """
        yesterday = datetime.now() - timedelta(1)
        if in_words:
            yesterday = datetime.strftime(yesterday, '%Y-%m-%d')
            kwargs = {
                'year': int(yesterday[:4]),
                'month': int(yesterday[5:7]),
                'day': int(yesterday[8:10])
            }
            return date(**kwargs).strftime('%A %d %B %Y')
        if obj:
            return yesterday
        return datetime.strftime(yesterday, '%Y-%m-%d')
    
    @staticmethod
    def today():
        """
        Get today's date

        Returns:
            datetime: formarted datetime object of todays date
        """
        return datetime.strftime(datetime.now(), '%Y-%m-%d')

    @staticmethod
    def start_time():
        """
        Get the day beforeyesterday's date

        Returns:
            datetime: formarted datetime object of the day before yesterday
        """
        return datetime.strftime(datetime.now() - timedelta(2), '%Y-%m-%d')


    @staticmethod
    def open_file(file_name_path):
        """
        Load data from a file given the `file_name_path`

        Args:
            file_name_path(str): string path to file including
                                 filename

        Returns:
            json: json data from file
        """
        with open(file_name_path) as file:
                data = json.load(file)
        return data

    @staticmethod
    def write_to_file(data, file_name):
        """
        Write json data to file

        Args:
            file_name(str): filename as a string
            data(json): data to be written to file

        Returns:
            None
        """
        with open(os.path.join(os.path.dirname(__file__), '../', 'storage', file_name), 'w') as file:
            json.dump(data, file)
    
    # @staticmethod
    # def reset_logs():
    #     """
    #     Reset log files

    #     Returns:
    #         None
    #     """
    #     logs_path = os.path.join(os.path.dirname(__file__), '../logs')
    #     for file_name in os.listdir(logs_path):
    #         os.system(f'cat /dev/null > {logs_path}/{file_name}')
    #         print(f'Log file {file_name} reset!')

