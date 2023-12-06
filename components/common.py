import tkinter as tk
import tkinter.ttk as ttk
import datetime
from typing import Literal
from utils.date import Date


def title_formater(title: str):
    if title == "":
        return "HeritageGenerator"
    return f"{title} - HeritageGenerator"


def big_btn_formater(text: str):
    return f"\n{text}\n"


class LabelAndEntry:
    def __init__(self, root: tk.BaseWidget, label_name: str, default_value: str | None = None) -> None:
        self.w = tk.Frame(root)
        self.__label = ttk.Label(self.w, text=label_name)
        self.__label.grid(row=0, column=0)
        self.__entry_var = tk.StringVar()
        if default_value != None:
            self.__entry_var.set(default_value)
        self.__entry = ttk.Entry(self.w, textvariable=self.__entry_var)
        self.__entry.grid(row=0, column=1, sticky=tk.EW)
        pass

    def get(self):
        return self.__entry_var.get()

    def set(self, x: str):
        return self.__entry_var.set(x)


class LabelAndDate:
    def __init__(self, root: tk.BaseWidget, label_name: str) -> None:
        self.w = tk.Frame(root)
        self.__label = ttk.Label(self.w, text=label_name)
        self.__label.grid(row=0, column=0)
        self.__var: dict[Literal["day"] | Literal["month"] | Literal["year"], tk.StringVar] = {"day": tk.StringVar(), "month": tk.StringVar(), "year": tk.StringVar()}
        self.__entries = {
            "day": ttk.Spinbox(self.w, from_=1, to=31, wrap=True, textvariable=self.__var["day"]),
            "month": ttk.Spinbox(self.w, from_=1, to=12, wrap=True, textvariable=self.__var["day"]),
            "year": ttk.Spinbox(self.w, from_=1, to=float(datetime.datetime.now().year), wrap=True, textvariable=self.__var["day"]),
        }
        self.__spacers = (ttk.Label(self.w, text="/"), ttk.Label(self.w, text="/"))
        self.__entries["day"].grid(row=0, column=1, sticky=tk.EW)
        self.__spacers[0].grid(row=0, column=2, sticky=tk.EW)
        self.__entries["day"].grid(row=0, column=3, sticky=tk.EW)
        self.__spacers[1].grid(row=0, column=4, sticky=tk.EW)
        self.__entries["day"].grid(row=0, column=5, sticky=tk.EW)
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
