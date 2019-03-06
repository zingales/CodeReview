import logging
import os
import errno
import json

logger = logging.getLogger(__name__)

# Taken from https://stackoverflow.com/a/600612/119527


def guarantee_folder(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class JsonConfigManager(object):

    PROJECTS_KEY_NAME = "project_paths"

    def __init__(self, folder, file):
        guarantee_folder(folder)
        self.file_path = os.path.join(folder, file)
        self._load_from_file()

    def _load_from_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path) as f:
                config = json.load(f)
        else:
            config = {}

        self.projects = config.get(self.PROJECTS_KEY_NAME, list())

    def save_to_file(self):
        toDump = dict()

        toDump[self.PROJECTS_KEY_NAME] = self.projects

        with open(self.file_path, 'w') as f:
            json.dump(toDump, f, indent=4, sort_keys=True)

    def add_project(self, path):
        self.projects.append(path)
