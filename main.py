import os
import sys
import logging
import time
from tkinter import Tk

from environment import Environment
from projectmanager import ProjectManager
from configmanager import JsonConfigManager
from gui import TkGui

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

CONFIG_FOLDER = "~/.CodeReview"

CONFIG_NAME = "config.json"

I_AM_EVAN = False


def old_school():
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


if __name__ == "__main__":
    config = JsonConfigManager(os.path.expanduser(CONFIG_FOLDER), CONFIG_NAME)
    if I_AM_EVAN:
        old_school()
    else:
        pm = ProjectManager(config)
        root = Tk()
        my_gui = TkGui(root, pm)
        root.mainloop()
        logger.info("Exiting")
        config.save_to_file()
