import tkinter as tk
import tkinter.ttk as ttk
from typing import Callable
from utils.person import Person
from components.common import LabelAndEntry, LabelAndButton, Button


class PersonDataDisplay:
    def __init__(self, root: tk.BaseWidget, person: Person, return_zone: Callable[[int], None]) -> None:
        self.person = person
        self.__return_zone = return_zone
        self.w = ttk.Labelframe(root, text=str(self.person))
        self.info: list[LabelAndEntry | LabelAndButton | Button] = [
            LabelAndEntry(self.w, "Id", str(self.person.id), readonly=True),
            LabelAndEntry(self.w, "First Name", self.person.first_name, readonly=True),
            LabelAndEntry(self.w, "Name", self.person.name, readonly=True),
            LabelAndEntry(self.w, "Old Name", self.person.old_name if self.person.old_name != None else "", readonly=True),
            LabelAndEntry(self.w, "Birth Date", self.person.birth_date.get_str() if self.person.birth_date != None else "", readonly=True),
            LabelAndEntry(self.w, "Birth Location", self.person.birth_location if self.person.birth_location != None else "", readonly=True),
            LabelAndEntry(self.w, "Death Date", self.person.death_date.get_str() if self.person.death_date != None else "", readonly=True),
            LabelAndEntry(self.w, "Death Location", self.person.death_location if self.person.death_location != None else "", readonly=True),
            LabelAndEntry(self.w, "Job", self.person.job if self.person.job != None else "", readonly=True),
            Button(self.w, "Select this", self.return_selected_person),
        ]
        for i in range(len(self.info)):
            if isinstance(self.info[i], Button):
                self.info[i].w.grid(row=i, column=0, sticky=tk.EW)
            else:
                self.info[i].w.grid(row=i, column=0, sticky=tk.E)
        pass

    def return_selected_person(self):
        self.__return_zone(self.person.id)
