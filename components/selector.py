import tkinter as tk
import tkinter.ttk as ttk
from utils.config import Language
from utils.person import Person, Family
from utils.watcher import Watcher


class SelectPerson:
    def __init__(self, root: tk.BaseWidget, lang: Language, list_person: dict[int, Person]) -> None:
        self.__persons = list_person
        self.w = ttk.Labelframe(root, text="Choose a person")
        self.columns = {
            "id": lang.get(["person", "terms", "id"]),
            "firstname": lang.get(["person", "terms", "first_name"]),
            "name": lang.get(["person", "terms", "name"]),
            "oldname": lang.get(["person", "terms", "old_name"]),
            "birthdate": lang.get(["person", "terms", "birth_date"]),
            "birthlocation": lang.get(["person", "terms", "birth_location"]),
            "deathdate": lang.get(["person", "terms", "death_date"]),
            "deathlocation": lang.get(["person", "terms", "death_location"]),
            "job": lang.get(["person", "terms", "job"]),
        }
        self.selected_person_id = Watcher(-1)
        self.tree = ttk.Treeview(self.w, columns=list(self.columns.keys()), show="headings")
        self.scrollbar = ttk.Scrollbar(self.w, orient="vertical", command=self.tree.yview)  # type: ignore
        self.tree["yscrollcommand"] = self.scrollbar.set
        self.__set_headings()
        self.__append_all_persons()
        self.tree.bind("<<TreeviewSelect>>", self.__person_selected)  # type: ignore
        self.tree.grid(row=0, column=0)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)
        pass

    def __set_headings(self):
        for i in range(len(self.columns)):
            self.tree.heading(list(self.columns.keys())[i], text=self.columns[list(self.columns.keys())[i]])
            self.tree.column(list(self.columns.keys())[i], width=(20 if list(self.columns.keys())[i] == "id" else 100))

    def __append_all_persons(self):
        formated_persons: list[tuple[int, str, str, str | None, str, str | None, str, str | None, str | None]] = []
        for person_id in self.__persons:
            person = self.__persons[person_id]
            formated_persons.append(
                (
                    person.id,
                    person.first_name,
                    person.name,
                    person.old_name if person.old_name != None else "",
                    person.birth_date.get_str() if person.birth_date != None else "",
                    person.birth_location if person.birth_location != None else "",
                    person.death_date.get_str() if person.death_date != None else "",
                    person.death_location if person.death_location != None else "",
                    person.job if person.job != None else "",
                )
            )
        for person in formated_persons:
            self.tree.insert("", tk.END, values=person)

    def __person_selected(self, event):  # type:ignore
        selected_person_data: list[int | str] = list(self.tree.item(self.tree.selection()[0]).values())[2]  # type: ignore
        self.selected_person_id.set(selected_person_data[0])  # type: ignore


class SelectFamily:
    def __init__(self, root: tk.BaseWidget, lang: Language, list_family: dict[int, Family]) -> None:
        self.__families = list_family
        self.w = ttk.Labelframe(root, text="Choose a family")
        self.columns = {
            "id": lang.get(["person", "terms", "id"]),
            "dad": lang.get(["families", "terms", "dad"]),
            "mom": lang.get(["families", "terms", "mom"]),
            "childs": lang.get(["families", "terms", "childs"]),
        }
        self.selected_family_id = Watcher(-1)
        self.tree = ttk.Treeview(self.w, columns=list(self.columns.keys()), show="headings")
        self.__set_headings()
        self.__append_all_families()
        self.tree.bind("<<TreeviewSelect>>", self.__family_selected)  # type: ignore
        self.tree.grid(row=0, column=0, sticky=tk.EW)
        pass

    def __set_headings(self):
        for i in range(len(self.columns)):
            self.tree.heading(list(self.columns.keys())[i], text=self.columns[list(self.columns.keys())[i]])
            if list(self.columns.keys())[i] == "id":
                self.tree.column(list(self.columns.keys())[i], width=20)
            elif list(self.columns.keys())[i] != "childs":
                self.tree.column(list(self.columns.keys())[i], width=120)
            else:
                self.tree.column(list(self.columns.keys())[i], width=240)

    def __format_childs(self, childs: list[Person]):
        if len(childs) == 0:
            return ""
        result = ""
        for child in childs:
            result += f"{child},"
        return result[:-1]

    def __append_all_families(self):
        formated_families: list[tuple[int, str, str, str]] = []
        for family_id in self.__families:
            family = self.__families[family_id]
            formated_families.append(
                (
                    family.id,
                    str(family.dad),
                    str(family.mom),
                    self.__format_childs(family.childs),
                )
            )
        for family in formated_families:
            self.tree.insert("", tk.END, values=family)

    def __family_selected(self, event):  # type:ignore
        selected_family_data: list[int | str] = list(self.tree.item(self.tree.selection()[0]).values())[2]  # type: ignore
        self.selected_family_id.set(selected_family_data[0])  # type: ignore
