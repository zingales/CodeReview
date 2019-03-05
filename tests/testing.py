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


def assert_head_reference(env, branch, hash, is_detached=False):
    assert str(env.repo.head.commit) == hash, "head hash is not what was expected: Expected {0}, actual {1}".format(
        hash, env.repo.head.commit)
    if not is_detached:
        assert str(env.repo.head.ref) == branch, "head branch is not what was expected: Expected {0}, actual {1}".format(
            branch, env.repo.head.ref)


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

    def test_switching_with_clean_repo(self):
        dir_path = os.path.join(self.repo_root, "switch_from_clean")
        env = Environment(dir_path)
        env.switch_to("branch_b")
        env.prepare_working_dir()
        assert_head_reference(
            env, 'master', 'e6a5ec02969059cd89375f60382c1ba11135dd08')

    def test_switching_with_clean_repo_with_stashes(self):
        dir_path = os.path.join(
            self.repo_root, "switch_from_clean_with_stashes")
        env = Environment(dir_path)
        env.switch_to("branch_b")
        env.prepare_working_dir()
        assert_head_reference(
            env, 'master', 'e6a5ec02969059cd89375f60382c1ba11135dd08')

    def test_detached_head_clean(self):
        dir_path = os.path.join(
            self.repo_root, "work_dir_is_detached")
        env = Environment(dir_path)
        env.switch_to("master")
        env.prepare_working_dir()
        assert_head_reference(
            env, 'n/a', 'e8605fa39902b240081ffb1894af0d28af4378a7', True)


if __name__ == '__main__':
    unittest.main()
