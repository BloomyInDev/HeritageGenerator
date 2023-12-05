import tkinter as tk
import tkinter.ttk as ttk
from components.common import *
from windows.edit_person import EditPersonWindow
from windows.gen_tree import GenTreeWindow
from utils.sql import Sql
from utils.tree import TreeGen


class Ui:
    def __init__(self) -> None:
        self.sql = Sql("data.db")

        self.persons = self.sql.get_all_persons()
        self.families = self.sql.get_all_families()
        self.tree = TreeGen(self.persons, self.families)

        self.w = tk.Tk()
        self.w.title(title_formater(""))
        self.w.resizable(False, False)
        self.ui_define_core_of_the_window()
        pass

    def refresh_data(self):
        self.person = self.sql.get_all_persons()
        self.families = self.sql.get_all_families()
        self.tree.update_persons(self.persons, self.families)

    def ui_define_core_of_the_window(self):
        add_person = ttk.Button(self.w, text=big_btn_formater("Add a person"), width=22, command=self.open_gentreewindow)
        add_person.grid(row=0, column=0, sticky=tk.NSEW)
        edit_person = ttk.Button(self.w, text=big_btn_formater("Edit a person"), width=22, command=self.open_editpersonwindow)
        edit_person.grid(row=0, column=1, sticky=tk.NSEW)
        generate_tree = ttk.Button(self.w, text=big_btn_formater("Generate Tree"), width=22, command=self.open_gentreewindow)
        generate_tree.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        pass

    def open_editpersonwindow(self):
        EditPersonWindow(self.w, self.persons)

    def open_gentreewindow(self):
        GenTreeWindow(self.w, self.tree)


if __name__ == "__main__":
    Ui()
    tk.mainloop()
