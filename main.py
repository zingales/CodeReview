import os
import sys
import logging
import time

from environment import Environment
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    code_path = sys.argv[1]
    assert os.path.isdir(code_path)

    # initial_commit = "39a14af872598b727a06ba87722edf4918dbedee"
    # code_path = os.path.dirname(os.path.abspath(__file__))

    env = Environment(code_path)

    print("to return to working dir just type revert")
    while True:
        text = input("paste reference id: ")
        if text == "revert":
            env.prepare_working_dir()
            continue
        env.switch_to(text)
