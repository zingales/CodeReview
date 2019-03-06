from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TkGui(object):

    def __init__(self, window, project_manager):
        self.pm = project_manager
        window.title("CodeReview")
        window.geometry('500x800')

        lbl = Label(window, text="Choose Project", font=("Arial Bold", 20))
        lbl.grid(column=0, row=0)
        combo = Combobox(window)
        self.project_chooser = combo
        combo['values'] = self.pm.list_projects()
        combo.grid(column=2, row=0)

        btn = Button(window, text="Add Project",
                     command=self.add_project_click)
        btn.grid(column=5, row=0)

    def add_project_click(self):
        dir = filedialog.askdirectory()
        logger.debug(dir)
        if dir:
            self.pm.add_project_from_path(dir)
            self.refresh_project_chooser()

    def refresh_project_chooser(self):
        self.project_chooser['values'] = self.pm.list_projects()
