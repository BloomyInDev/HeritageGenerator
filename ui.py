import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo, showerror  # type: ignore
from components.common import *
import windows.file as file
from windows.person import AddPersonWindow, EditPersonWindow
from windows.families import FamiliesWindow
from windows.gen_tree import GenTreeWindow
from windows.about import AboutWindow
from utils.ui_template import UiTemplate
from utils.file import FileLoader
from utils.sql import Sql
from utils.person import Person
from utils.tree import TreeGen
from utils.config import Config, Language


class Ui(UiTemplate):
    def __init__(self) -> None:
        self.sql: Sql
        self.file_loader = FileLoader()
        self.tree: TreeGen | None = None  # = TreeGen(self.persons, self.families)
        self.cfg = Config()
        self.lang = Language(self.cfg.get(["lang"]))
        self.w = tk.Tk()
        self.w.focus()
        self.w.title(title_formater(""))
        self.w.iconphoto(True, tk.PhotoImage(file="./assets/icon.png"))
        self.w.resizable(False, False)
        self.w.protocol("WM_DELETE_WINDOW", self.ui_close_app)

        self.content_frame = ttk.Frame(self.w)
        self.ui_define_menu()
        self.ui_define_core_of_the_window()
        self.content_frame.grid(row=0, column=0, padx=5, pady=5)
        pass

    def update_person(self, person: Person):
        self.sql.edit_person(person)

    def refresh_data(self):
        if not isinstance(self.tree, TreeGen):
            self.tree = TreeGen(self, self.sql.get_all_persons(), self.sql.get_all_families())
        else:
            self.tree.update_persons(self.sql.get_all_persons(), self.sql.get_all_families())
        print(f"Loaded {len(self.tree.get_persons())} persons and {len(self.tree.get_families())} families")
        pass

    def change_btn_state(self, disabled: bool):
        for e in [self.__add_person_btn, self.__edit_person_btn, self.__edit_families_btn, self.__generate_tree_btn]:
            e.configure(state="disabled" if disabled else "normal")
        pass

    def ui_define_menu(self):
        self.menu = tk.Menu(self.w, tearoff=False)
        self.w.config(menu=self.menu)
        file_menu = tk.Menu(self.menu, tearoff=False)
        file_menu.add_command(label=self.lang.get(["menu", "file", "new-file"]), command=self.ui_new_file)
        file_menu.add_command(label=self.lang.get(["menu", "file", "open"]), command=self.ui_open_file)
        file_menu.add_command(label=self.lang.get(["menu", "file", "save"]), command=self.ui_save_file)
        file_menu.add_separator()
        file_menu.add_command(label=self.lang.get(["menu", "file", "close"]), command=self.w.destroy)
        self.menu.add_cascade(label=self.lang.get(["menu", "file", "name"]), menu=file_menu)
        act_menu = tk.Menu(self.menu, tearoff=False)
        act_menu.add_command(label=self.lang.get(["home", "add-person"]), command=lambda: Bootstraper().create_person(self.file_loader, self))
        act_menu.add_command(label=self.lang.get(["home", "edit-person"]), command=lambda: Bootstraper().edit_person(self.file_loader, self))
        act_menu.add_command(label=self.lang.get(["home", "gen-tree"]), command=lambda: Bootstraper().gen_tree(self.file_loader, self))
        self.menu.add_cascade(label=self.lang.get(["menu", "actions", "name"]), menu=act_menu)
        self.menu.add_command(label=self.lang.get(["menu", "about", "name"]), command=lambda: AboutWindow(self.w, self))

    def ui_define_core_of_the_window(self):
        self.__add_person_btn = ttk.Button(
            self.content_frame,
            text=big_btn_formater(self.lang.get(["home", "add-person"])),
            width=22,
            command=lambda: Bootstraper().create_person(self.file_loader, self),
        )
        self.__add_person_btn.grid(row=0, column=0, sticky=tk.NSEW)
        self.__edit_person_btn = ttk.Button(
            self.content_frame,
            text=big_btn_formater(self.lang.get(["home", "edit-person"])),
            width=22,
            command=lambda: Bootstraper().edit_person(self.file_loader, self),
        )
        self.__edit_person_btn.grid(row=0, column=1, sticky=tk.NSEW)
        self.__edit_families_btn = ttk.Button(
            self.content_frame,
            text=big_btn_formater("Families"),
            width=22,
            command=lambda: Bootstraper().edit_families(self.file_loader, self),
        )
        self.__edit_families_btn.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self.__generate_tree_btn = ttk.Button(
            self.content_frame,
            text=big_btn_formater(self.lang.get(["home", "gen-tree"])),
            width=22,
            command=lambda: Bootstraper().gen_tree(self.file_loader, self),
        )
        self.__generate_tree_btn.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW)
        self.change_btn_state(not self.file_loader.file_loaded)
        pass

    def ui_new_file(self):
        # TODO make this method
        pass

    def ui_open_file(self):
        self.sql = file.OpenFile(self, self.file_loader)
        self.refresh_data()
        self.change_btn_state(not self.file_loader.file_loaded)

    def ui_save_file(self):
        file.SaveFile(self, self.file_loader)
        self.change_btn_state(not self.file_loader.file_loaded)
        self.tree = None

    def ui_close_app(self):
        if file.CloseApp(self, self.file_loader):
            self.w.destroy()


class Bootstraper:
    def __init__(self) -> None:
        pass

    def create_person(self, file_loader: FileLoader, ui: Ui):
        if file_loader.file_loaded:
            AddPersonWindow(ui.w, ui.sql)
        else:
            showerror(title_formater(ui.lang.get(["error", "title"])), ui.lang.get(["error", "no-file-loaded"]))

    def edit_person(self, file_loader: FileLoader, ui: Ui):
        if file_loader.file_loaded:
            EditPersonWindow(ui.w, ui.sql)
        else:
            showerror(title_formater(ui.lang.get(["error", "title"])), ui.lang.get(["error", "no-file-loaded"]))

    def edit_families(self, file_loader: FileLoader, ui: Ui):
        if file_loader.file_loaded:
            FamiliesWindow(ui.w, ui)
        else:
            showerror(title_formater(ui.lang.get(["error", "title"])), ui.lang.get(["error", "no-file-loaded"]))
        pass

    def gen_tree(self, file_loader: FileLoader, ui: Ui):
        if file_loader.file_loaded:
            assert isinstance(ui.tree, TreeGen)
            GenTreeWindow(ui.w, ui)
        else:
            showerror(title_formater(ui.lang.get(["error", "title"])), ui.lang.get(["error", "no-file-loaded"]))


if __name__ == "__main__":
    Ui()
    tk.mainloop()
