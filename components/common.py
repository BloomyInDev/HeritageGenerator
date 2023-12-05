import tkinter as tk
import tkinter.ttk as ttk
import datetime


def title_formater(title: str):
    return "HeritageGenerator" if title == "" else f"{title} - HeritageGenerator"


def big_btn_formater(text: str):
    return f"\n{text}\n"


class LabelAndEntry:
    def __init__(self, root: tk.BaseWidget, label_name: str) -> None:
        self.w = tk.Frame(root)
        self.__label = ttk.Label(self.w, text=label_name)
        self.__label.grid(row=0, column=0)
        self.__entry_var = tk.StringVar()
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
        self.__entry_var = tk.StringVar()
        self.__var = {"day": tk.StringVar(), "month": tk.StringVar(), "year": tk.StringVar()}
        self.__entries = {
            "day": ttk.Spinbox(self.w, from_=1, to=31, wrap=True, textvariable=self.__var["day"]),
            "month": ttk.Spinbox(self.w, from_=1, to=12, wrap=True, textvariable=self.__var["day"]),
            "year": ttk.Spinbox(self.w, from_=1, to=datetime.datetime.now().year, wrap=True, textvariable=self.__var["day"]),
        }
        self.__spacers = (ttk.Label(self.w, text="/"), ttk.Label(self.w, text="/"))
        self.__entries["day"].grid(row=0, column=1, sticky=tk.EW)
        self.__spacers[0].grid(row=0, column=2, sticky=tk.EW)
        self.__entries["day"].grid(row=0, column=3, sticky=tk.EW)
        self.__spacers[1].grid(row=0, column=4, sticky=tk.EW)
        self.__entries["day"].grid(row=0, column=5, sticky=tk.EW)
        pass
