import os
import logging

from git import Repo
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

code_path = os.path.dirname(os.path.abspath(__file__))

repo = Repo(code_path)


def has_initial_commit(repo):
    try:
        repo.head.commit
    except ValueError as ve:
        return False
    return True


def preserve(repo):
    assert not repo.bare, "repo is bare"
    assert has_initial_commit(repo), "Repo has not been initialized"
    if not repo.is_dirty():
        logging.debug("nothing to preserve")
        return None

    stash_name = "stashy_mcstash"
    logging.debug("preserving changes")
    logging.debug(repo.git.stash('push', '-m', stash_name))


def switch_repo(repo, cr_id):
    preserve(repo)


switch_repo(repo, "bob")
