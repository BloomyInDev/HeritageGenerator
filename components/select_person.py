import tkinter as tk
import tkinter.ttk as ttk
from utils.person import Person
from utils.watcher import Watcher

columns = {
    "id": "Id",
    "firstname": "First Name",
    "name": "Name",
    "oldname": "Old Name",
    "birthdate": "Birth Date",
    "birthlocation": "Birth Location",
    "deathdate": "Death Date",
    "deathlocation": "Death Location",
    "job": "Job",
}


class SelectPerson:
    def __init__(self, root: tk.BaseWidget, list_person: dict[int, Person]) -> None:
        self.__persons = list_person
        self.w = ttk.Labelframe(root, text="Choose a person")
        self.selected_person_id = Watcher(-1)
        self.tree = ttk.Treeview(self.w, columns=list(columns.keys()), show="headings")
        self.__set_headings()
        self.__append_all_persons()
        self.tree.bind("<<TreeviewSelect>>", self.__person_selected)  # type: ignore
        self.tree.grid(row=0, column=0)
        pass

    def __set_headings(self):
        for i in range(len(columns)):
            self.tree.heading(list(columns.keys())[i], text=columns[list(columns.keys())[i]])
            self.tree.column(list(columns.keys())[i], width=(20 if list(columns.keys())[i] == "id" else 100))

    def __append_all_persons(self):
        formated_persons: list[tuple[int, str, str, str | None, str, str | None, str, str | None, str | None]] = []
        for person_id in self.__persons:
            person = self.__persons[person_id]
            formated_persons.append(
                (
                    person.id,
                    person.first_name,
                    person.name,
                    person.old_name,
                    person.birth_date.get_str() if person.birth_date != None else "Unknown",
                    person.birth_location if person.birth_location != None else "Unknown",
                    person.death_date.get_str() if person.death_date != None else "Unknown",
                    person.death_location if person.death_location != None else "Unknown",
                    person.job if person.job != None else "Unknown",
                )
            )
        for person in formated_persons:
            self.tree.insert("", tk.END, values=person)

    def __person_selected(self, event):  # type:ignore
        selected_person_data: list[int | str] = list(self.tree.item(self.tree.selection()[0]).values())[2]  # type: ignore
        self.selected_person_id.set(selected_person_data[0])  # type: ignore
