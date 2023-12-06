import tkinter as tk
import tkinter.ttk as ttk
from utils.person import Person
from components.common import LabelAndEntry


class PersonDataDisplay:
    def __init__(self, root: tk.BaseWidget, person: Person) -> None:
        self.person = person
        self.w = ttk.Labelframe(root, text=f"Information about {str(self.person)}")
        self.info: list[LabelAndEntry] = [
            LabelAndEntry(self.w, "Id", str(self.person.id)),
            LabelAndEntry(self.w, "First Name", self.person.first_name),
            LabelAndEntry(self.w, "Name", self.person.name),
            LabelAndEntry(self.w, "Old Name", self.person.old_name if self.person.old_name != None else "Unknown"),
        ]
        pass
