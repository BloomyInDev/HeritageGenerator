import tkinter as tk
from typing import Literal
from utils.person import Person
from utils.sql import Sql
from components.selector import SelectPerson
from components.person_data import PersonDataEditor, PersonDataCreator


class AddPersonWindow:
    def __init__(self, root: tk.Tk, sql: Sql) -> None:
        self.w = tk.Toplevel(root)
        self.addzone = PersonDataCreator(self.w, max(sql.get_all_persons().keys()) + 1, sql.create_new_person)
        self.addzone.w.grid()


class EditPersonWindow:
    def __init__(self, root: tk.Tk, sql: Sql) -> None:
        list_person = sql.get_all_persons()
        print(list_person)
        self.w = tk.Toplevel(root)
        self.__persons = list_person
        self.__sql = sql
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

    def validate(self, act: Literal["update", "delete"], person: Person):
        match act:
            case "update":
                self.__sql.edit_person(person)
                self.__persons = self.__sql.get_all_persons()
                self.select_person.w.destroy()
            case "delete":
                self.__sql.delete_person(person.id)

        self.select_person = SelectPerson(self.w, self.__persons)
        self.select_person.w.grid(row=0, column=0)
        # print(str(person))
