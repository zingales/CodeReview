from tkinter import *
from tkinter import ttk
# import Combobox, Notebook, Frame
from tkinter import filedialog, messagebox
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TkGui(object):

    def __init__(self, window, project_manager):
        self.pm = project_manager
        window.title("CodeReview")
        window.geometry('500x800')

        base_frame = ttk.Frame(window)
        top_frame = ttk.Frame(base_frame)
        top_frame.grid(column=0, row=0)
        lbl = Label(top_frame, text="Choose Project", font=("Arial Bold", 20))
        lbl.grid(column=0, row=0)
        # combo = ttk.Combobox(window)
        # self.project_chooser = combo
        # combo['values'] = self.pm.list_projects()
        # combo.grid(column=2, row=0)
        #
        # btn = Button(window, text="Add Project",
        #              command=self.add_project_click)
        # btn.grid(column=5, row=0)
        # btn_load_proj = Button(window, text="Load Project",
        #                        command=self.load_project)
        # btn_load_proj.grid(column=5, row=1)

        bottom_frame = ttk.Frame(base_frame)
        bottom_frame.grid(column=0, row=2)
        self.tab_control = ttk.Notebook(bottom_frame)
        tab_control = self.tab_control
        # tab1 = ttk.Frame(self.tab_control)
        # self.tab_control.add(tab1, text='Info')
        # self.tab_control.pack(expand=1, fill='both')

        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='First')
        tab_control.add(tab2, text='Second')
        lbl1 = Label(tab1, text='label1')
        lbl1.grid(column=0, row=0)
        lbl2 = Label(tab2, text='label2')
        lbl2.grid(column=0, row=0)

        base_frame.pack()
        self.tabs = list()

    def remove_selected_tab_from_view(self):
        self.tab_control.forget(self.tab_control.select())

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

        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text=selection)
        self.tabs.append(TabManager(tab, self.pm.get_env_from_path(selection)))


class TabManager(object):

    def __init__(self, tab, env):
        self.tab = tab
        self.env = env
        refresh_button = Button(
            self.tab, text="Refresh/Fetch", command=self.env.fetch)
        refresh_button.grid(column=0, row=0)
