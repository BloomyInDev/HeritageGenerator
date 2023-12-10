import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo  # type: ignore
from components.common import *
from windows.edit_person import EditPersonWindow
from windows.gen_tree import GenTreeWindow
from windows.about import AboutWindow
from utils.sql import Sql
from utils.person import Person
from utils.tree import TreeGen


class Ui:
    def __init__(self) -> None:
        self.sql = Sql("data.db")

        self.persons = self.sql.get_all_persons()
        self.families = self.sql.get_all_families()
        self.tree = TreeGen(self.persons, self.families)

        self.w = tk.Tk()
        self.w.title(title_formater(""))
        self.w.iconphoto(True, tk.PhotoImage(file="./assets/icon.png"))
        self.w.resizable(False, False)

        self.content_frame = ttk.Frame(self.w)
        self.ui_define_menu()
        self.ui_define_core_of_the_window()
        self.content_frame.grid(row=0, column=0, padx=5, pady=5)
        pass

    def update_person(self, person: Person):
        self.sql.edit_person(person)

    def refresh_data(self):
        self.person = self.sql.get_all_persons()
        self.families = self.sql.get_all_families()
        self.tree.update_persons(self.persons, self.families)

    def ui_define_menu(self):
        self.menu = tk.Menu(self.w, tearoff=False)
        self.w.config(menu=self.menu)
        file_menu = tk.Menu(self.menu, tearoff=False)
        file_menu.add_command(label="Open", command=lambda: showinfo(title_formater("Info"), "Not implemented"))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.w.destroy)
        self.menu.add_cascade(label="File", menu=file_menu)
        act_menu = tk.Menu(self.menu, tearoff=False)
        act_menu.add_command(label="Add a person", command=lambda: GenTreeWindow(self.w, self.tree))
        act_menu.add_command(label="Edit a person", command=lambda: EditPersonWindow(self.w, self.persons))
        act_menu.add_command(label="Generate Tree", command=lambda: GenTreeWindow(self.w, self.tree))
        self.menu.add_cascade(label="Actions", menu=act_menu)
        self.menu.add_command(label="About", command=lambda: AboutWindow(self.w))

    def ui_define_core_of_the_window(self):
        add_person = ttk.Button(self.content_frame, text=big_btn_formater("Add a person"), width=22, command=lambda: GenTreeWindow(self.w, self.tree))
        add_person.grid(row=0, column=0, sticky=tk.NSEW)
        edit_person = ttk.Button(self.content_frame, text=big_btn_formater("Edit a person"), width=22, command=lambda: EditPersonWindow(self.w, self.persons))
        edit_person.grid(row=0, column=1, sticky=tk.NSEW)
        generate_tree = ttk.Button(self.content_frame, text=big_btn_formater("Generate Tree"), width=22, command=lambda: GenTreeWindow(self.w, self.tree))
        generate_tree.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        pass


if __name__ == "__main__":
    Ui()
    tk.mainloop()
