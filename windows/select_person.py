import tkinter as tk
from typing import Callable
from utils.config import Language
from utils.person import Person
from components.selector import SelectPerson
from components.person_data import PersonDataDisplay


class SelectPersonWindow:
    def __init__(self, root: tk.Tk, lang: Language, list_person: dict[int, Person], return_zone: Callable[[int], None], with_none: bool = False) -> None:
        self.w = tk.Toplevel(root)
        self.__return_zone = return_zone
        self.__persons = list_person
        if with_none:
            self.__persons = {-1: Person(-1, "", "None")} | list_person
        self.person_selected: Person
        self.select_person = SelectPerson(self.w, lang, list_person)
        self.select_person.w.grid(row=0, column=0)
        self.select_person.selected_person_id.watch_changes(self.on_change)
        self.right_part: PersonDataDisplay | None = None
        pass

    def on_change(self):
        self.person_selected = self.__persons[self.select_person.selected_person_id.get()]  # type: ignore
        if self.right_part != None:
            self.right_part.w.destroy()
        print("Changing person")
        self.right_part = PersonDataDisplay(self.w, self.person_selected, self.validate)
        self.right_part.w.grid(row=0, column=1, sticky=tk.NSEW)

    def validate(self, person_id: int):
        self.__return_zone(person_id)
        self.w.destroy()
