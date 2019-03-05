import sys
import shutil
import os
import tempfile
import unittest
import logging

sys.path.append('..')
from environment import Environment  # noqa: E402

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TestRepos(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # make temp folder
        temp_folder = tempfile.mkdtemp()
        cls.repo_root = os.path.join(temp_folder, "repos")

        # copy repos folder to temporary location
        current_folder = os.path.dirname(os.path.abspath(__file__))
        source_repos = os.path.join(current_folder, "repos")

        shutil.copytree(source_repos, cls.repo_root)
        print("temp dir", cls.repo_root)

        # rename all git folders to .git folders
        for fname in os.listdir(cls.repo_root):
            path = os.path.join(cls.repo_root, fname)
            if os.path.isdir(path):
                os.rename(os.path.join(path, "git"),
                          os.path.join(path, ".git"))

    def test_empty_repo(self):
        dir_path = os.path.join(self.repo_root, "empty_repo")
        env = Environment(dir_path)
        with self.assertRaises(AssertionError):
            env.preserve_working_dir("notneeded")

    def test_fail_on_dirty_no_initial(self):
        dir_path = os.path.join(self.repo_root, "no_initial_commit_dirty")
        env = Environment(dir_path)
        with self.assertRaises(AssertionError):
            env.preserve_working_dir("notneeded")


if __name__ == '__main__':
    unittest.main()
