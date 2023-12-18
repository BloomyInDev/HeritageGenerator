import tkinter as tk
import tkinter.ttk as ttk
from typing import Callable, Literal
from utils.person import Person
from utils.ui_template import UiTemplate

person_types = {"mom": "Mom", "dad": "Dad", "childs": "Childs"}


class FamilyPart:
    def __init__(self, root: tk.BaseWidget, ui: UiTemplate, who: Literal["mom", "dad", "granddad", "grandmom"], person: Person | None, callback: Callable[[], None]) -> None:
        self.w = ttk.Frame(root)
        self.btn = ttk.Button(self.w, text=person_types[who], command=callback)
        self.btn.grid(row=0, column=0, sticky=tk.NSEW)
        self.text = tk.StringVar(value=str(person))
        self.entry = ttk.Entry(self.w, textvariable=self.text, state="disabled")
        # self.label = ttk.Label(self.w, text=str(person if person != None else "Unknow"))
        self.entry.grid(row=1, column=0, sticky=tk.NSEW)
        self.w.configure(relief="solid", borderwidth=2)
        pass


class ChildPart:
    def __init__(self, root: tk.BaseWidget, ui: UiTemplate, list_childs: list[Person], callback: Callable[[], None]) -> None:
        self.w = ttk.Frame(root)
        self.btn = ttk.Button(self.w, text=person_types["childs"], command=callback)
        self.btn.grid(row=0, column=0, sticky=tk.NSEW)
        self.list_var = tk.Variable(value=list_childs)
        self.list = tk.Listbox(self.w, listvariable=self.list_var, selectmode=tk.SINGLE, height=len(list_childs))
        self.list.grid(row=1, column=0, sticky=tk.NSEW)
        self.w.configure(relief="solid", borderwidth=2)
        pass
