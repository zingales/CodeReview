import logging

logger = logging.getLogger(__name__)


def has_initial_commit(repo):
    try:
        repo.head.commit
    except ValueError as ve:
        return False
    return True


def gen_preserve_event(current_commit):
    return ("preserve", current_commit)


def gen_switch_event(destination_id):
    return ("switch", destination_id)


class Environment(object):

    def __init__(self, repo):
        self.repo = repo
        self.history = []
        self.starting_branch = None

    def preserve_working_dir(self, stash_name):
        assert not self.repo.bare, "repo is bare"
        assert has_initial_commit(self.repo), "Repo has not been initialized"
        if not self.repo.is_dirty():
            logger.debug("nothing to preserve")
            return False

        head_commit = self.repo.head.commit
        logger.debug("preserving changes")
        logger.debug(self.repo.git.stash('push', '-m', stash_name))
        self.history.append(gen_preserve_event(head_commit))
        return True

    def switch_to(self, cr_id):
        if self.starting_branch is None:
            stash_name = self.gen_stash_name("working", cr_id)
            self.preserve_working_dir(stash_name)
            self.starting_branch = self.repo.head.ref
        self.repo.git.checkout(cr_id)
        self.history.append(gen_switch_event(cr_id))

    def gen_stash_name(self, source_id, destination_id):
        return "{0}->{1}".format(source_id, destination_id)

    def prepare_working_dir(self):
        self.repo.git.checkout(self.starting_branch)
        self.starting_branch = None
        self.repo.git.stash('pop')
