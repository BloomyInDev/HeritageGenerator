import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from typing import Callable, Literal
from utils.config import Language
from utils.person import Person
from utils.date import Date, compare_dates
from components.common import LabelAndEntry, LabelAndButton, Button, DateEntry, Entry, big_btn_formater, title_formater


class PersonDataDisplay:
    def __init__(self, root: tk.BaseWidget, lang: Language, person: Person, return_zone: Callable[[int], None]) -> None:
        self.person = person
        self.__return_zone = return_zone
        self.w = ttk.Labelframe(root, text=str(self.person))
        self.info: list[LabelAndEntry | LabelAndButton | Button] = [
            LabelAndEntry(self.w, lang.get(["person", "terms", "id"]), str(self.person.id), readonly=True),
            LabelAndEntry(self.w, lang.get(["person", "terms", "first_name"]), self.person.first_name, readonly=True),
            LabelAndEntry(self.w, lang.get(["person", "terms", "name"]), self.person.name, readonly=True),
            LabelAndEntry(self.w, lang.get(["person", "terms", "old_name"]), self.person.old_name if self.person.old_name != None else "", readonly=True),
            LabelAndEntry(self.w, lang.get(["person", "terms", "birth_date"]), self.person.birth_date.get_str() if self.person.birth_date != None else "", readonly=True),
            LabelAndEntry(self.w, lang.get(["person", "terms", "birth_location"]), self.person.birth_location if self.person.birth_location != None else "", readonly=True),
            LabelAndEntry(self.w, lang.get(["person", "terms", "death_date"]), self.person.death_date.get_str() if self.person.death_date != None else "", readonly=True),
            LabelAndEntry(self.w, lang.get(["person", "terms", "death_location"]), self.person.death_location if self.person.death_location != None else "", readonly=True),
            LabelAndEntry(self.w, lang.get(["person", "terms", "job"]), self.person.job if self.person.job != None else "", readonly=True),
            Button(self.w, lang.get(["person", "terms", "select"]), self.return_selected_person),
        ]
        for i in range(len(self.info)):
            if isinstance(self.info[i], Button):
                self.info[i].w.grid(row=i, column=0, sticky=tk.EW)
            else:
                self.info[i].w.grid(row=i, column=0, sticky=tk.E)
        pass

    def return_selected_person(self):
        self.__return_zone(self.person.id)


class PersonDataCreator:
    def __init__(self, root: tk.BaseWidget, lang: Language, id_person: int, return_zone: Callable[[Person], None]) -> None:
        self.__return_zone = return_zone
        self.__root = root
        self.w = ttk.Labelframe(root, text="Add a person")
        self.label = [
            ttk.Label(self.w, text=lang.get(["person", "terms", "id"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "first_name"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "name"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "old_name"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "birth_date"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "birth_location"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "death_date"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "death_location"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "job"])),
        ]
        self.info: list[Entry | DateEntry] = [
            Entry(self.w, default_value=str(id_person), readonly=True),
            Entry(self.w),
            Entry(self.w),
            Entry(self.w),
            DateEntry(self.w),
            Entry(self.w),
            DateEntry(self.w),
            Entry(self.w),
            Entry(self.w),
        ]
        for i in range(len(self.label)):
            self.label[i].grid(row=i, column=0, sticky=tk.E)
        for i in range(len(self.info)):
            self.info[i].w.grid(row=i, column=1, sticky=tk.NSEW)
        self.btn = ttk.Button(self.w, text=big_btn_formater(lang.get(["add-person", "add"])), command=self.return_new_person)
        self.btn.grid(row=len(self.info), column=0, columnspan=2, sticky=tk.NSEW)
        pass

    def return_new_person(self):
        # id = self.info[0].get()
        # first_name = self.info[1].get()
        # new_person = Person(,self.info[2].get(),self.info[1].get())
        assert isinstance(self.info[0], Entry)
        assert isinstance(self.info[4], DateEntry) and isinstance(self.info[6], DateEntry)
        assert isinstance(self.info[1], Entry) and isinstance(self.info[2], Entry)
        assert isinstance(self.info[3], Entry) and isinstance(self.info[5], Entry)
        assert isinstance(self.info[7], Entry) and isinstance(self.info[8], Entry)

        if self.info[1].get() == "":
            return msgbox.showerror(title_formater("Error"), "First name can't be empty")  # type: ignore
        if self.info[2].get() == "":
            return msgbox.showerror(title_formater("Error"), "Name can't be empty")  # type: ignore

        new_person = Person(
            int(self.info[0].get()),
            self.info[2].get(),
            self.info[1].get(),
            self.info[3].get() if self.info[3].get() != "" else None,
            self.info[4].get() if compare_dates(self.info[4].get(), Date(0, 0, 0, ignoreassert=True)) == False else None,
            self.info[5].get() if self.info[5].get() != "" else None,
            self.info[6].get() if compare_dates(self.info[6].get(), Date(0, 0, 0, ignoreassert=True)) == False else None,
            self.info[7].get() if self.info[7].get() != "" else None,
            self.info[8].get() if self.info[8].get() != "" else None,
        )

        self.__return_zone(new_person)
        msgbox.showinfo(title_formater("Info"), message="Person added sucessfully !")  # type: ignore
        self.__root.destroy()


class PersonDataEditor:
    def __init__(self, root: tk.BaseWidget, lang: Language, person: Person, return_zone: Callable[[Literal["update", "delete"], Person], None]) -> None:
        self.person = person
        self.__return_zone = return_zone
        self.w = ttk.Labelframe(root, text=str(self.person))
        self.label = [
            ttk.Label(self.w, text=lang.get(["person", "terms", "id"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "first_name"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "name"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "old_name"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "birth_date"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "birth_location"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "death_date"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "death_location"])),
            ttk.Label(self.w, text=lang.get(["person", "terms", "job"])),
        ]
        self.info: tuple[
            Entry,
            Entry,
            Entry,
            Entry,
            DateEntry,
            Entry,
            DateEntry,
            Entry,
            Entry,
        ] = (
            Entry(self.w, str(self.person.id), readonly=True),
            Entry(self.w, self.person.first_name),
            Entry(self.w, self.person.name),
            Entry(self.w, self.person.old_name if self.person.old_name != None else ""),
            DateEntry(self.w, self.person.birth_date if self.person.birth_date != None else Date(0, 0, 0, ignoreassert=True)),
            Entry(self.w, self.person.birth_location if self.person.birth_location != None else ""),
            DateEntry(self.w, self.person.death_date if self.person.death_date != None else Date(0, 0, 0, ignoreassert=True)),
            Entry(self.w, self.person.death_location if self.person.death_location != None else ""),
            Entry(self.w, self.person.job if self.person.job != None else ""),
        )
        for i in range(len(self.label)):
            self.label[i].grid(row=i, column=0, sticky=tk.E)
        for i in range(len(self.info)):
            self.info[i].w.grid(row=i, column=1, sticky=tk.NSEW)
        self.btn_frame = ttk.Frame(self.w)
        self.save_btn = ttk.Button(self.btn_frame, text=lang.get(["person", "save"]), command=self.return_updated_person)
        self.save_btn.grid(row=0, column=0, sticky=tk.NSEW)
        self.del_btn = ttk.Button(self.btn_frame, text=lang.get(["person", "del"]), command=self.return_deleted_person)
        self.del_btn.grid(row=0, column=1, sticky=tk.NSEW)
        self.files_btn = ttk.Button(self.btn_frame, text=lang.get(["person","files"]), command=self.open_files_menu)
        self.btn_frame.grid(row=len(self.info), column=0, columnspan=2, sticky=tk.NSEW)

        pass

    def return_deleted_person(self):
        if msgbox.askokcancel(title=title_formater("Are you sure ?"), message=f"Are you sure to delete {self.person} ?"):  # type: ignore
            self.__return_zone("delete", self.person)
        else:
            pass

    def return_updated_person(self):
        assert isinstance(self.info[4], DateEntry) and isinstance(self.info[6], DateEntry)
        assert isinstance(self.info[1], Entry) and isinstance(self.info[2], Entry)
        assert isinstance(self.info[3], Entry) and isinstance(self.info[5], Entry)
        assert isinstance(self.info[7], Entry) and isinstance(self.info[8], Entry)

        if self.info[1].get() == "":
            return msgbox.showerror(title_formater("Error"), "First name can't be empty")  # type: ignore
        if self.info[2].get() == "":
            return msgbox.showerror(title_formater("Error"), "Name can't be empty")  # type: ignore

        person = Person(
            int(self.info[0].get()),
            self.info[2].get(),
            self.info[1].get(),
            self.info[3].get() if self.info[3].get() != "" else None,
            self.info[4].get() if self.info[4].get() != Date(0, 0, 0, ignoreassert=True) else None,
            self.info[5].get() if self.info[5].get() != "" else None,
            self.info[6].get() if self.info[6].get() != Date(0, 0, 0, ignoreassert=True) else None,
            self.info[7].get() if self.info[7].get() != "" else None,
            self.info[8].get() if self.info[8].get() != "" else None,
        )
        self.__return_zone("update", person)

    def open_files_menu(self):
        
        pass