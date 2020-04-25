import json
from config import AppConfig
from datetime import datetime, timedelta
from api.utils import Util

class DataStore(Util):
    def __init__(self):
        self.data = Util.open_file(AppConfig.ORGANIZATIONS)
        self.projects = Util.open_file(AppConfig.PROJECTS)
        self.activities = Util.open_file(AppConfig.ACTIVITIES)

    def get_organizations(self):
        return self.data['organizations']

    def get_projects(self):
        return self.projects['projects']

    def get_users(self):
        users = []
        for organization in self.get_organizations():
            users += [user for user in organization['users']]
        return users

    def get_activities(self):
        return self.activities['activities']
    
    def get_data(self):
        organisations = self.get_organizations()
        return [ self.add_projects(org) for org in organisations], Util.yesterday(True)

    
    def format_project_user(self, user, project):
        activities = self.get_activities()
        duration = sum([activity['tracked'] for activity in activities if activity['user_id'] == user['id'] and project['id'] == activity['project_id']])

        return {
            'id':user['id'],
            'name': user['name'],
            'logged': str(timedelta(seconds=duration))
        }

    def format_project(self, project):
        users = [self.format_project_user(user, project) for user in self.get_users()]
        return {
            'id': project['id'],
            'name': project['name'],
            'users': users
        }


    def add_projects(self, org):
        org['projects'] = [ self.format_project(project) for project in self.get_projects()]
        org['users'] = [Util.format_user(user) for user in org['users']]
        return org
