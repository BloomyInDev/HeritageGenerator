import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo, showerror  # type: ignore
from components.common import *
from windows.file import OpenFile, SaveFile
from windows.person import AddPersonWindow, EditPersonWindow
from windows.gen_tree import GenTreeWindow
from windows.about import AboutWindow
from utils.file import FileLoader
from utils.sql import Sql
from utils.person import Person
from utils.tree import TreeGen


class Ui:
    def __init__(self) -> None:
        self.sql: Sql
        self.file_loader = FileLoader()
        self.tree: TreeGen | None = None  # = TreeGen(self.persons, self.families)

        self.w = tk.Tk()
        self.w.focus()
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
        if not isinstance(self.tree, TreeGen):
            self.tree = TreeGen(self.sql.get_all_persons(), self.sql.get_all_families())
        else:
            self.tree.update_persons(self.sql.get_all_persons(), self.sql.get_all_families())
        print(f"Loaded {len(self.tree.get_persons())} persons and {len(self.tree.get_families())} families")
        pass

    def change_btn_state(self, disabled: bool):
        for e in [self.__add_person_btn, self.__edit_person_btn, self.__generate_tree_btn]:
            e.configure(state="disabled" if disabled else "normal")
        pass

    def ui_define_menu(self):
        self.menu = tk.Menu(self.w, tearoff=False)
        self.w.config(menu=self.menu)
        file_menu = tk.Menu(self.menu, tearoff=False)
        file_menu.add_command(label="Open", command=self.ui_open_file)
        file_menu.add_command(label="Save", command=self.ui_save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.w.destroy)
        self.menu.add_cascade(label="File", menu=file_menu)
        act_menu = tk.Menu(self.menu, tearoff=False)
        act_menu.add_command(label="Add a person", command=lambda: Bootstraper().create_person(self.file_loader, self.w, self.sql))
        act_menu.add_command(label="Edit a person", command=lambda: Bootstraper().edit_person(self.file_loader, self.w, self.sql))
        act_menu.add_command(label="Generate Tree", command=lambda: Bootstraper().gen_tree(self.file_loader, self.w, self.tree))
        self.menu.add_cascade(label="Actions", menu=act_menu)
        self.menu.add_command(label="About", command=lambda: AboutWindow(self.w))

    def ui_define_core_of_the_window(self):
        self.__add_person_btn = ttk.Button(
            self.content_frame, text=big_btn_formater("Add a person"), width=22, command=lambda: Bootstraper().create_person(self.file_loader, self.w, self.sql)
        )
        self.__add_person_btn.grid(row=0, column=0, sticky=tk.NSEW)
        self.__edit_person_btn = ttk.Button(
            self.content_frame, text=big_btn_formater("Edit a person"), width=22, command=lambda: Bootstraper().edit_person(self.file_loader, self.w, self.sql)
        )
        self.__edit_person_btn.grid(row=0, column=1, sticky=tk.NSEW)
        self.__generate_tree_btn = ttk.Button(
            self.content_frame, text=big_btn_formater("Generate Tree"), width=22, command=lambda: Bootstraper().gen_tree(self.file_loader, self.w, self.tree)
        )
        self.__generate_tree_btn.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self.change_btn_state(not self.file_loader.file_loaded)
        pass

    def ui_open_file(self):
        self.sql = OpenFile(self.file_loader)
        self.refresh_data()
        self.change_btn_state(not self.file_loader.file_loaded)

    def ui_save_file(self):
        SaveFile(self.sql, self.file_loader)
        self.change_btn_state(not self.file_loader.file_loaded)
        self.tree = None


class Bootstraper:
    def __init__(self) -> None:
        pass

    def create_person(self, file_loader: FileLoader, root: tk.Tk, sql: Sql):
        if file_loader.file_loaded:
            AddPersonWindow(root, sql)
        else:
            showerror(title_formater("Error"), "You need to open a file to do that !")

    def edit_person(self, file_loader: FileLoader, root: tk.Tk, sql: Sql):
        if file_loader.file_loaded:
            EditPersonWindow(root, sql)
        else:
            showerror(title_formater("Error"), "You need to open a file to do that !")

    def gen_tree(self, file_loader: FileLoader, root: tk.Tk, tree: TreeGen | None):
        if file_loader.file_loaded:
            assert isinstance(tree, TreeGen)
            GenTreeWindow(root, tree)
        else:
            showerror(title_formater("Error"), "You need to open a file to do that !")


if __name__ == "__main__":
    Ui()
    tk.mainloop()
