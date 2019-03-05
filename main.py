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

    env = Environment(code_path)

    howto = '''
To help you view and run Code Review locally
How to use:
* Enter git reference id (Hash or branch) for the code you'd like to review.
* To return to you working directory type revert
* To quit type exit
    '''
    print(howto)
    while True:
        text = input("paste reference id: ")
        if text == "revert":
            env.prepare_working_dir()
            continue
        elif text == "exit":
            if env.starting_branch is not None:
                if 'y' == input("we've not retuned to the working branch exit anyway? (y/n)"):
                    break
            else:
                break
        elif text == "help":
            print(howto)
        else:
            env.switch_to(text)
