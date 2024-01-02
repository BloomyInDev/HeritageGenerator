import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from typing import Callable, Literal
from components.common import title_formater
from windows.select_person import SelectPersonWindow
from utils.person import Person
from utils.ui_template import UiTemplate


class FamilyPart:
    def __init__(
        self,
        root: tk.BaseWidget,
        ui: UiTemplate,
        who: Literal["mom", "dad", "granddad", "grandmom"],
        person: Person | None,
        callback: Callable[[int], None],
        direction: Literal["horizontal", "vertical"] = "vertical",
    ) -> None:
        self.w = ttk.Frame(root)
        self.__callback, self.__ui = callback, ui
        self.person_types = {
            "mom": ui.lang.get(["families", "terms", "mom"]),
            "dad": ui.lang.get(["families", "terms", "dad"]),
            "childs": ui.lang.get(["families", "terms", "childs"]),
        }
        self.btn = ttk.Button(self.w, text=self.person_types[who], command=self.on_click)  # lambda: callback(person.id if person != None else -1))
        self.btn.grid(row=0, column=0, sticky=tk.NSEW)
        self.person = person
        self.text = tk.StringVar(value=str(self.person))
        self.entry = ttk.Entry(self.w, textvariable=self.text, state="disabled")
        # self.label = ttk.Label(self.w, text=str(person if person != None else "Unknow"))
        self.entry.grid(row=1 if direction == "vertical" else 0, column=0 if direction == "vertical" else 1, sticky=tk.NSEW)
        self.w.configure(relief="solid", borderwidth=2)
        pass

    def on_click(self):
        self.select_person = SelectPersonWindow(self.__ui.w, self.__ui.lang, self.__ui.sql.get_all_persons(), self.on_return, True)

    def on_return(self, person_id: int):
        self.person = self.__ui.sql.get_all_persons()[person_id]
        self.text.set(str(self.person))
        self.select_person.w.destroy()
        self.__callback(person_id)


class ChildPart:
    def __init__(
        self,
        root: tk.BaseWidget,
        ui: UiTemplate,
        list_childs: list[Person],
        callback: Callable[[int, Literal["add", "remove"]], None],
        direction: Literal["horizontal", "vertical"] = "vertical",
    ) -> None:
        self.__list_childs = list_childs
        self.__callback = callback
        self.__ui = ui
        self.person_types = {
            "mom": ui.lang.get(["families", "terms", "mom"]),
            "dad": ui.lang.get(["families", "terms", "dad"]),
            "childs": ui.lang.get(["families", "terms", "childs"]),
        }
        self.w = ttk.Frame(root)
        self.btn = ttk.Button(self.w, text=self.person_types["childs"])
        self.btn.grid(row=0, column=0, columnspan=1 if direction == "vertical" else 2, sticky=tk.NSEW)
        self.list_var = tk.Variable(value=list_childs)
        self.list = tk.Listbox(self.w, listvariable=self.list_var, selectmode=tk.SINGLE, height=len(list_childs))
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
        self.select_person = SelectPersonWindow(self.__ui.w, self.__ui.lang, self.__ui.sql.get_all_persons(), self.add_btn_return)
        pass

    def add_btn_return(self, person_id: int):
        self.__callback(person_id, "add")

    def remove_btn_click(self):
        tk_person_selected = self.list.curselection()  # type: ignore
        if len(tk_person_selected) == 1:  # type: ignore
            self.__callback(self.__list_childs[self.list.curselection()[0]].id, "remove")  # type: ignore
            pass
        else:
            msgbox.showerror(  # type: ignore
                title=title_formater(self.__ui.lang.get(["error", "title"])),
                message=self.__ui.lang.get(["error", "no-person-selected"]),
            )
            pass
