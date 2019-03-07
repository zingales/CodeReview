# from tkinter import *
from tkinter import ttk
from tkinter.ttk import Button
import os
# import Combobox, Notebook, Frame
from tkinter import filedialog, messagebox, Label, Entry
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TkGui(object):

    def __init__(self, window, project_manager):
        self.pm = project_manager
        window.title("CodeReview")
        window.geometry('600x400')

        self.tab_control = ttk.Notebook(window)
        tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(tab1, text='Main')
        lbl = Label(tab1, text="Choose Project", font=("Arial Bold", 20))
        lbl.grid(column=0, row=0)
        combo = ttk.Combobox(tab1)
        self.project_chooser = combo
        combo['values'] = self.pm.list_projects()
        combo.grid(column=2, row=0)

        btn = Button(tab1, text="Add Project",
                     command=self.add_project_click)
        btn.grid(column=5, row=0)
        btn_load_proj = Button(tab1, text="Load Project",
                               command=self.load_project)
        btn_load_proj.grid(column=5, row=1)
        self.tab_control.pack(expand=1, fill='both')
        self.tabs = list()

        for x in self.pm.list_projects():
                self._load_project(x)

    def add_project_click(self):
        dir = filedialog.askdirectory()
        logger.debug(dir)
        if dir:
            self.pm.add_project_from_path(dir)
            self.refresh_project_chooser()

    def refresh_project_chooser(self):
        self.project_chooser['values'] = self.pm.list_projects()

    def load_project(self):
        selection = self.project_chooser.get()
        logger.debug(selection)
        if not selection:
            messagebox.showerror('Error', "No Project selected")
            return
        return self._load_project(selection)

    def _load_project(self, path):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text=os.path.basename(path))
        self.tabs.append(TabManager(tab, self.pm.get_env_from_path(path)))


class TabManager(object):

    def __init__(self, tab, env):
        self.tab = tab
        self.env = env
        lbl = Label(self.tab, text="Project Path: {0}".format(
            env.path), font=("Arial Bold", 10))
        lbl.grid(column=0, row=0)
        refresh_button = Button(
            self.tab, text="Fetch", command=self.fetch)
        refresh_button.grid(column=2, row=0)
        self.current_branch = Label(self.tab)
        self.current_branch.grid(column=1, row=0)

        lbl = Label(self.tab, text="Choose Branch To View")
        lbl.grid(column=0, row=1)
        self.branch_chooser = ttk.Combobox(self.tab)
        self.branch_chooser.grid(column=1, row=1)

        lbl = Label(self.tab, text="Choose Commit To View")
        lbl.grid(column=0, row=2)
        self.commit_entry = Entry(self.tab, width=20)
        self.commit_entry.grid(column=1, row=2)
        commit_button = Button(
            self.tab, text="switch", command=self.switch)
        commit_button.grid(column=0, row=3)
        commit_button = Button(
            self.tab, text="revert", command=self.revert)
        commit_button.grid(column=0, row=4)

        self.refresh()

    def fetch(self):
        self.env.fetch()
        self.refresh()

    def refresh(self):
        names = self.env.get_branch_names()
        names.insert(0, "")
        self.branch_chooser['values'] = names
        self.current_branch.configure(
            text="Current Branch {0}".format(self.env.current_branch()))

    def switch(self):
        branch = self.branch_chooser.get()
        if branch:
            self.env.switch_to(branch)
        else:
            commit = self.commit_entry.get()
            if not commit:
                messagebox.showerror('Error', "No reference to switch to")
            else:
                self.env.switch_to(commit)
        self.refresh()

    def revert(self):
        try:
            self.env.prepare_working_dir()
        except ValueError:
            messagebox.showerror(
                'Error', "Cannot revert if we havne't switched to anything")
        self.refresh()
