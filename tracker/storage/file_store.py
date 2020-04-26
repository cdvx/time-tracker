"""Module for DataStore"""

import json
from config import AppConfig
from datetime import datetime, timedelta
from tracker.utils import Util

class DataStore:
    """Class to manage data used by the application"""

    def __init__(self):
        # assign data attributes to instance
        self.data = Util.open_file(AppConfig.ORGANIZATIONS)
        self.projects = Util.open_file(AppConfig.PROJECTS)
        self.activities = Util.open_file(AppConfig.ACTIVITIES)

    def get_organizations(self):
        """
        Get organizations the user is attached to

        Returns:
            list: results list of organization(s)
        """
        return self.data['organizations']

    def get_projects(self):
        """
        Get projects the user is attached to

        Returns:
            list: results list of projects(s)
        """
        return self.projects['projects']

    def get_users(self):
        """
        Get organisation users who have been logging time

        Returns:
            list: results list of users(s)
        """
        users = []
        for organization in self.get_organizations():
            users += [user for user in organization['users']]
        return users

    def get_activities(self):
        """
        Get time logging activites data

        Returns:
            list: results list of activities(s)
        """
        return self.activities['activities']
    
    def get_data(self):
        """
        Get structured data with information on
            1: the organisation
            2: the projects
            3: the users

        Returns:
            list: results list of organization object(s)
                  with relevant data
        """
        organisations = self.get_organizations()
        return [ self.add_projects(org) for org in organisations], Util.yesterday(in_words=True)

    
    def format_project_user(self, user, project):
        """
        Format a project user, adding necessary attributes
        Adds time logged by a user on a given project from 
        activities data.

        Args:
            user(dict): current user in iteration
            project(dict): current project in iteration

        Returns:
            dict: structured user dict
        """
        activities = self.get_activities()
        duration = sum([activity['tracked'] for activity in activities if self.valid_activity(activity, user, project)])

        return {
            'id':user['id'],
            'name': user['name'],
            'logged': str(timedelta(seconds=duration))
        }

    def format_project(self, project):
        """
        Format a project, adding necessary attributes
        Adds a list of formatted users on a given project

        Args:
            project(dict): current project in iteration

        Returns:
            dict: strutured project dict
        """
        users = [self.format_project_user(user, project) for user in self.get_users()]
        return {
            'id': project['id'],
            'name': project['name'],
            'users': users
        }
    def active_project(self, project):
        """
        Check activity on a given project

        Args:
            project(dict): current project in iteration

        Returns:
            bool: True if project has some activity else False 
        """
        for user in project['users']:
            if user['logged'] != '0:00:00':
                return True
        return False

    def add_projects(self, org):
        """
        Add active projects to the organization object

        Args:
            org(dict): current organization in iteration

        Returns:
            dict: strutured organization dict with active
                  projects and fprmatted users
        """
        org['projects'] = list(filter(self.active_project, [ self.format_project(project) for project\
             in self.get_projects()]))
        org['users'] = [Util.format_user(user) for user in org['users']]
        return org

    def valid_activity(self, activity, user, project):
        """
        Check validity of activity basing on the the ativity
        timeslot. Valid if it corresponds to yesterday

        Args:
            activity(dict): current activity in iteration
            user(dict): current user in iteration
            project(dict): current project in iteration

        Returns:
            bool: True if activity is valid else False
        """
        date = activity['time_slot']
        activity_date = datetime.fromisoformat(date.replace('Z', '+00:00')).replace(tzinfo=None)

        user_matches_activity = activity['user_id'] == user['id']
        project_matches_activity = project['id'] == activity['project_id']
        yesterdays_activity = activity_date >= datetime.combine(Util.yesterday(obj=True), datetime.min.time())

        if user_matches_activity and project_matches_activity and yesterdays_activity:
            return True
        return False

