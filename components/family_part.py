import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from typing import Callable, Literal
from components.common import title_formater
from windows.select_person import SelectPersonWindow
from utils.person import Person
from utils.ui_template import UiTemplate

person_types = {"mom": "Mom", "dad": "Dad", "childs": "Childs"}


class FamilyPart:
    def __init__(self, root: tk.BaseWidget, ui: UiTemplate, who: Literal["mom", "dad", "granddad", "grandmom"], person: Person | None, callback: Callable[[int], None]) -> None:
        self.w = ttk.Frame(root)
        self.btn = ttk.Button(self.w, text=person_types[who], command=lambda: callback(person.id if person != None else -1))
        self.btn.grid(row=0, column=0, sticky=tk.NSEW)
        self.text = tk.StringVar(value=str(person))
        self.entry = ttk.Entry(self.w, textvariable=self.text, state="disabled")
        # self.label = ttk.Label(self.w, text=str(person if person != None else "Unknow"))
        self.entry.grid(row=1, column=0, sticky=tk.NSEW)
        self.w.configure(relief="solid", borderwidth=2)
        pass


class ChildPart:
    def __init__(self, root: tk.BaseWidget, ui: UiTemplate, list_childs: list[Person], callback: Callable[[int, Literal["add", "remove"]], None]) -> None:
        self.__list_childs = list_childs
        self.__callback = callback
        self.__ui = ui
        self.w = ttk.Frame(root)
        self.btn = ttk.Button(self.w, text=person_types["childs"])
        self.btn.grid(row=0, column=0, sticky=tk.NSEW)
        self.list_var = tk.Variable(value=list_childs)
        self.list = tk.Listbox(self.w, listvariable=self.list_var, selectmode=tk.SINGLE, height=len(list_childs))
        self.list.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)
        self.btn_rem = ttk.Button(self.w, text="-", width=1, command=self.remove_btn_click)
        self.btn_rem.grid(row=0, column=1, sticky=tk.NSEW)
        self.btn_add = ttk.Button(self.w, text="+", width=1, command=self.add_btn_click)
        self.btn_add.grid(row=0, column=2, sticky=tk.NSEW)
        self.w.configure(relief="solid", borderwidth=2)
        pass

    def add_btn_click(self):
        self.select_person = SelectPersonWindow(self.__ui.w, self.__ui.sql.get_all_persons(), self.add_btn_return)
        pass

    def add_btn_return(self, person_id: int):
        self.__callback(person_id, "add")

    def remove_btn_click(self):
        tk_person_selected = self.list.curselection()  # type: ignore
        if len(tk_person_selected) == 1:  # type: ignore
            self.__callback(self.__list_childs[self.list.curselection()[0]], "remove")  # type: ignore
            pass
        else:
            msgbox.showerror(  # type: ignore
                title=title_formater(self.__ui.lang.get(["error", "title"])),
                message=self.__ui.lang.get(["error", "no-person-selected"]),
            )
            pass
