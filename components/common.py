import tkinter as tk
import tkinter.ttk as ttk
import datetime
from typing import Literal, Callable
from utils.date import Date


def title_formater(title: str):
    if title == "":
        return "HeritageGenerator"
    return f"{title} - HeritageGenerator"


def big_btn_formater(text: str):
    return f"\n{text}\n"


class LabelAndEntry:
    def __init__(self, root: tk.BaseWidget, label_name: str, default_value: str | None = None, readonly: bool = False) -> None:
        self.w = tk.Frame(root)
        self.__label = ttk.Label(self.w, text=label_name)
        self.__label.grid(row=0, column=0, sticky=tk.W)
        self.__entry_var = tk.StringVar()
        if default_value != None:
            self.__entry_var.set(default_value)

        self.__entry = ttk.Entry(self.w, textvariable=self.__entry_var)
        if readonly:
            self.__entry.configure(state="readonly")
        self.__entry.grid(row=0, column=1, sticky=tk.EW)
        pass

    def get(self):
        return self.__entry_var.get()

    def set(self, x: str):
        return self.__entry_var.set(x)


class LabelAndDate:
    def __init__(self, root: tk.BaseWidget, label_name: str, date: Date | None = None) -> None:
        self.w = tk.Frame(root)
        self.__label = ttk.Label(self.w, text=label_name)
        self.__label.grid(row=0, column=0)
        self.__var: dict[Literal["day"] | Literal["month"] | Literal["year"], tk.StringVar] = {"day": tk.StringVar(), "month": tk.StringVar(), "year": tk.StringVar()}
        self.__entries = {
            "day": ttk.Spinbox(self.w, from_=1, to=31, wrap=True, textvariable=self.__var["day"], width=5),
            "month": ttk.Spinbox(self.w, from_=1, to=12, wrap=True, textvariable=self.__var["month"], width=5),
            "year": ttk.Spinbox(self.w, from_=1, to=float(datetime.datetime.now().year), wrap=True, textvariable=self.__var["year"], width=5),
        }
        self.__spacers = (ttk.Label(self.w, text="/"), ttk.Label(self.w, text="/"))
        self.__entries["day"].grid(row=0, column=1, sticky=tk.EW)
        self.__spacers[0].grid(row=0, column=2, sticky=tk.EW)
        self.__entries["month"].grid(row=0, column=3, sticky=tk.EW)
        self.__spacers[1].grid(row=0, column=4, sticky=tk.EW)
        self.__entries["year"].grid(row=0, column=5, sticky=tk.EW)
        pass

    def get(self):
        return Date(int(self.__var["day"].get()), int(self.__var["month"].get()), int(self.__var["year"].get()))

    def set_with_Date(self, date: Date):
        self.__var["day"].set(str(date.get_day()))
        self.__var["month"].set(str(date.get_month()))
        self.__var["year"].set(str(date.get_year()))

    def set(self, day: int, month: int, year: int):
        self.__var["day"].set(str(day))
        self.__var["month"].set(str(month))
        self.__var["year"].set(str(year))
        pass


class DateEntry:
    def __init__(self, root: tk.BaseWidget, date: Date | None = None) -> None:
        self.w = tk.Frame(root)
        self.__var: dict[Literal["day"] | Literal["month"] | Literal["year"], tk.StringVar] = {"day": tk.StringVar(), "month": tk.StringVar(), "year": tk.StringVar()}
        self.__entries = {
            "day": ttk.Spinbox(self.w, from_=1, to=31, wrap=True, textvariable=self.__var["day"], width=5),
            "month": ttk.Spinbox(self.w, from_=1, to=12, wrap=True, textvariable=self.__var["month"], width=5),
            "year": ttk.Spinbox(self.w, from_=1, to=float(datetime.datetime.now().year), wrap=True, textvariable=self.__var["year"], width=5),
        }
        self.__spacers = (ttk.Label(self.w, text="/"), ttk.Label(self.w, text="/"))
        self.__entries["day"].grid(row=0, column=0, sticky=tk.EW)
        self.__spacers[0].grid(row=0, column=1, sticky=tk.EW)
        self.__entries["month"].grid(row=0, column=2, sticky=tk.EW)
        self.__spacers[1].grid(row=0, column=3, sticky=tk.EW)
        self.__entries["year"].grid(row=0, column=4, sticky=tk.EW)
        pass

    def get(self):
        return Date(int(self.__var["day"].get()), int(self.__var["month"].get()), int(self.__var["year"].get()))

    def set_with_Date(self, date: Date):
        self.__var["day"].set(str(date.get_day()))
        self.__var["month"].set(str(date.get_month()))
        self.__var["year"].set(str(date.get_year()))

    def set(self, day: int, month: int, year: int):
        self.__var["day"].set(str(day))
        self.__var["month"].set(str(month))
        self.__var["year"].set(str(year))
        pass


class Entry:
    def __init__(self, root: tk.BaseWidget, default_value: str | None = None, readonly: bool = False):
        self.__entry_var = tk.StringVar()
        self.w = ttk.Entry(root, textvariable=self.__entry_var)
        if readonly:
            self.w.configure(state="readonly")
        if default_value != None:
            self.__entry_var.set(default_value)
        pass

    def get(self):
        return self.__entry_var.get()

    def set(self, x: str):
        return self.__entry_var.set(x)


class Button:
    def __init__(self, root: tk.BaseWidget, btn_text: str, btn_command: Callable[[], None]) -> None:
        self.w = ttk.Button(root, text=btn_text, command=btn_command)
        pass


class LabelAndButton:
    def __init__(self, root: tk.BaseWidget, label_text: str, button_name: str, btn_command: Callable[[], None]) -> None:
        self.w = tk.Frame(root)
        self.__label = ttk.Label(self.w, text=label_text)
        self.__label.grid(row=0, column=0, sticky=tk.W)
        self.__btn = ttk.Button(self.w, text=button_name, command=btn_command)
        self.__btn.grid(row=0, column=0, sticky=tk.EW)
        pass
