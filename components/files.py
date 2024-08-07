import tkinter as tk
from tkinter import ttk, messagebox as msgbox, filedialog as fdiag
from typing import Callable, Literal
from components.common import title_formater
from utils.file import FileInDb, create_file_template, remove_file
from utils.person import Person
from utils.ui_template import UiTemplate


class PersonDataFileList:
    def __init__(
        self,
        root: tk.BaseWidget,
        ui: UiTemplate,
        person: Person,
        list_files: list[FileInDb],
        callback: Callable[[FileInDb, Literal["add", "remove"]], None],
        direction: Literal["horizontal", "vertical"] = "vertical",
    ) -> None:
        self.__list_files = list_files
        self.__callback = callback
        self.__ui = ui
        self.person = person
        self.w = ttk.Frame(root)
        self.btn = ttk.Button(self.w, text=self.__ui.lang.get(["additional-files", "file"]))
        self.btn.grid(row=0, column=0, columnspan=1 if direction == "vertical" else 2, sticky=tk.NSEW)
        self.list_var = tk.Variable(value=list(map(lambda x: x.name, list_files)))
        self.list = tk.Listbox(self.w, listvariable=self.list_var, selectmode=tk.SINGLE, height=len(list_files))
        self.list.grid(
            row=1 if direction == "vertical" else 0,
            column=0 if direction == "vertical" else 2,
            columnspan=3 if direction == "vertical" else 2,
            rowspan=2 if direction == "horizontal" else 1,
            sticky=tk.NSEW,
        )
        self.btn_rem = ttk.Button(self.w, text="-", width=1, command=self.remove_btn_click)
        self.btn_rem.grid(row=0 if direction == "vertical" else 1, column=1 if direction == "vertical" else 0, sticky=tk.NSEW)
        self.btn_add = ttk.Button(self.w, text="+", width=1, command=self.add_btn_click)
        self.btn_add.grid(row=0 if direction == "vertical" else 1, column=2 if direction == "vertical" else 1, sticky=tk.NSEW)
        self.w.configure(relief="solid", borderwidth=2)
        pass

    def add_btn_click(self):
        fpath = fdiag.askopenfilename(
            title=title_formater(self.__ui.lang.get(["diag", "open", "title"])),
            filetypes=((self.__ui.lang.get(["files", "pdf-files"]), "*.pdf"), (self.__ui.lang.get(["files", "all-files"]), "*.*")),
        )
        f = create_file_template(fpath, self.person.id)
        if f != None:
            self.__callback(f, "add")

        pass

    def add_btn_return(self, f: FileInDb):
        print(f)
        self.__callback(f, "add")

    def remove_btn_click(self):
        tk_person_selected = self.list.curselection()  # type: ignore
        if len(tk_person_selected) == 1:  # type: ignore
            f: FileInDb = self.__list_files[self.list.curselection()[0]]  # type: ignore
            if isinstance(f, FileInDb):
                remove_file(f)
                self.__callback(f, "remove")
            pass
        else:
            msgbox.showerror(  # type: ignore
                title=title_formater(self.__ui.lang.get(["error", "title"])),
                message=self.__ui.lang.get(["error", "no-person-selected"]),
            )
            pass
