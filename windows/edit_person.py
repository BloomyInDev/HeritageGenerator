import tkinter as tk
from utils.person import Person
from components.select_person import SelectPerson
from components.person_data import PersonDataEditor


class EditPersonWindow:
    def __init__(self, root: tk.Tk, list_person: dict[int, Person]) -> None:
        self.w = tk.Toplevel(root)
        self.__persons = list_person
        self.person_selected: Person
        self.select_person = SelectPerson(self.w, list_person)
        self.select_person.w.grid(row=0, column=0)
        self.select_person.selected_person_id.watch_changes(self.on_change)
        self.right_part: PersonDataEditor | None = None
        pass

    def on_change(self):
        self.person_selected = self.__persons[self.select_person.selected_person_id.get()]  # type: ignore
        if self.right_part != None:
            self.right_part.w.destroy()
        print("Changing person")
        self.right_part = PersonDataEditor(self.w, self.person_selected, self.validate)
        self.right_part.w.grid(row=0, column=1, sticky=tk.NSEW)

    def validate(self, person: Person):
        print(str(person))
