import tkinter as tk
import tkinter.ttk as ttk
from typing import Callable
from utils.person import Person
from components.common import LabelAndEntry, LabelAndButton, Button, DateEntry, Entry


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


class PersonDataEditor:
    def __init__(self, root: tk.BaseWidget, person: Person, return_zone: Callable[[Person], None]) -> None:
        self.person = person
        self.__return_zone = return_zone
        self.w = ttk.Labelframe(root, text=str(self.person))
        self.label = [
            ttk.Label(self.w, text="Id"),
            ttk.Label(self.w, text="First Name"),
            ttk.Label(self.w, text="Name"),
            ttk.Label(self.w, text="Old Name"),
            ttk.Label(self.w, text="Birth Date"),
            ttk.Label(self.w, text="Birth Location"),
            ttk.Label(self.w, text="Death Date"),
            ttk.Label(self.w, text="Death Location"),
            ttk.Label(self.w, text="Job"),
        ]
        self.info: list[Entry | DateEntry] = [
            Entry(self.w, str(self.person.id), readonly=True),
            Entry(self.w, self.person.first_name),
            Entry(self.w, self.person.name),
            Entry(self.w, self.person.old_name if self.person.old_name != None else ""),
            DateEntry(self.w, self.person.birth_date),
            Entry(self.w, self.person.birth_location if self.person.birth_location != None else ""),
            DateEntry(self.w, self.person.birth_date),
            Entry(self.w, self.person.death_location if self.person.death_location != None else ""),
            Entry(self.w, self.person.job if self.person.job != None else ""),
        ]
        for i in range(len(self.label)):
            self.label[i].grid(row=i, column=0, sticky=tk.E)
        for i in range(len(self.info)):
            self.info[i].w.grid(row=i, column=1, sticky=tk.NSEW)
        pass

    def return_updated_person(self):
        assert isinstance(self.info[0], LabelAndEntry)
        # id = self.info[0].get()
        # first_name = self.info[1].get()
        # new_person = Person(,self.info[2].get(),self.info[1].get())
        self.__return_zone(self.person)
