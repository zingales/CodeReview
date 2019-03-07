import logging
from git import Repo
import re
import os

logger = logging.getLogger(__name__)


def has_initial_commit(repo):
    try:
        repo.head.commit
    except ValueError as ve:
        return False
    return True


# def gen_preserve_event(current_commit):
#     return ("preserve", current_commit)
#
#
# def gen_switch_event(destination_id):
#     return ("switch", destination_id)


class Environment(object):

    working_dir_id = "Work Dir"

    def __init__(self, git_path):
        self.path = git_path
        assert os.path.isdir(git_path), "path provided is not a directory"
        assert os.path.exists(os.path.join(git_path, ".git")
                              ), "no git info in root folder"

        self.repo = Repo(git_path)
        # self.history = []
        self.starting_branch = None
        self.starting_dirty = None

    def preserve_working_dir(self, stash_name):
        assert not self.repo.bare, "repo is bare"
        assert has_initial_commit(self.repo), "Repo has not been initialized"
        if not self.repo.is_dirty():
            logger.debug("nothing to preserve")
            return False

        head_commit = self.repo.head.commit
        logger.debug("preserving changes")
        logger.debug(self.repo.git.stash('push', '-m', stash_name))
        # self.history.append(gen_preserve_event(head_commit))
        return True

    def switch_to(self, cr_id):
        if self.starting_branch is None:
            stash_name = self.gen_stash_name(self.working_dir_id, cr_id)
            logging.debug(stash_name)
            self.starting_dirty = self.preserve_working_dir(stash_name)
            if self.repo.head.is_detached:
                self.starting_branch = self.repo.head.commit
            else:
                self.starting_branch = self.repo.head.ref
        self.repo.git.checkout(cr_id)
        # self.history.append(gen_switch_event(cr_id))

    def gen_stash_name(self, source_id, destination_id):
        return "CR:{0}->{1}".format(source_id, destination_id)

    def current_branch(self):
        try:
            return self.repo.active_branch.name
        except TypeError:
            return "No Branch"

    def find_working_dir_stash(self):
        return self.stash_name_to_stash_index(
            self.gen_stash_name(self.working_dir_id, ''))

    def get_branch_names(self):
        return [h.name for h in self.repo.heads]

    def stash_name_to_stash_index(self, stash_prefix):
        stash_response = self.repo.git.stash('list')
        if len(stash_response) == 0:
            raise ValueError("No stashes to be searched")

        for line in stash_response.split('\n'):
            # from IPython import embed
            # embed()
            m = re.search(r"stash@\{(\d+)\}: (.+): (.*)", line)
            assert m, "error in matching git stash line:" + line
            if m.group(3).startswith(stash_prefix):
                return m.group(1)

        raise ValueError(
            "Could not find a stash name that matched: " + stash_prefix)

    def prepare_working_dir(self):
        if self.starting_branch is None:
            raise ValueError(
                "Cannot revert from an when we haven't switched to anything")

        self.repo.git.checkout(self.starting_branch)
        self.starting_branch = None
        if self.starting_dirty:
            num = self.find_working_dir_stash()
            self.repo.git.stash('pop', 'stash@{{{0}}}'.format(num))
            self.starting_dirty = None

    def fetch(self):
        for remote in self.repo.remotes:
            logger.debug("fetching: " + str(remote))
            remote.fetch()
