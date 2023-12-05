import tkinter as tk
import tkinter.ttk as ttk
import time, multiprocessing
from components.common import *
from components.preview import PreviewWindow
from utils.sql import Sql
from utils.tree import TreeGen


class Ui:
    def __init__(self) -> None:
        sql = Sql("data.db")

        self.persons = sql.get_all_persons()
        self.families = sql.get_all_families()
        self.tree = TreeGen(self.persons, self.families)

        self.w = tk.Tk(title_formater(""))
        self.w.resizable(False, False)
        self.ui_define_core_of_the_window()
        pass

    def ui_define_core_of_the_window(self):
        generate_tree = ttk.Button(self.w, text=home_menu_btn_formater("Generate Tree"), width=22, command=self.generate_and_display_tree)
        generate_tree.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        pass

    def generate_and_display_tree(self):
        file_path = self.tree.gen_tree("full", None, "png", False)
        if file_path != None:
            PreviewWindow(self.w, file_path)


if __name__ == "__main__":
    ctx = multiprocessing.get_context("spawn")
    q = ctx.Queue()
    Ui()
    tk.mainloop()
