import tkinter as tk
import tkinter.ttk as ttk
from utils.person import Person
from components.select_person import SelectPerson


class EditPersonWindow:
    def __init__(self, root: tk.Tk, list_person: dict[int, Person]) -> None:
        self.w = tk.Toplevel(root)
        self.__persons = list_person
        self.person_selected: Person
        self.select_person = SelectPerson(self.w, list_person)
        self.select_person.w.grid(row=0, column=0)
        self.select_person.selected_person_id.watch_changes(self.on_change)
        self.right_part: ttk.Labelframe | None = None
        pass

    def on_change(self):
        self.person_selected = self.__persons[self.select_person.selected_person_id.get()]  # type: ignore
        if self.right_part != None:
            self.right_part.destroy()
        self.right_part = ttk.Labelframe(self.w)
