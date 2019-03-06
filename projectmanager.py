import os
import logging

from environment import Environment

logger = logging.getLogger(__name__)


class ProjectManager(object):

    def __init__(self, config):
        self.projects = [Environment(dir_path) for dir_path in config.projects]
        self.config = config

    def add_project_from_path(self, dir_path):
        env = Environment(dir_path)
        self.projects.append(env)
        self.config.add_project(dir_path)

    def list_projects(self):
        return [x.path for x in self.projects]

    def get_env_from_path(self, path):
        for env in self.projects:
            if env.path == path:
                return env
