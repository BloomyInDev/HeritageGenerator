import tkinter as tk
import tkinter.ttk as ttk
from typing import Literal
from components.common import title_formater
from utils.person import Person
from utils.ui_template import UiTemplate
from components.selector import SelectFamily
from components.family_part import ChildPart, FamilyPart
from windows.select_person import SelectPersonWindow
from PIL import Image, ImageTk

coords_for_persons: dict[Literal["mom", "dad", "childs"], tuple[float, float]] = {
    "dad": (75, 50),
    "mom": (75, 150),
    "childs": (325, 100),
}


class FamiliesWindow:
    def __init__(self, root: tk.Tk, ui: UiTemplate) -> None:
        self.__ui = ui
        self.w = tk.Toplevel(root, width=500)
        self.__ui = ui
        self.w.title(title_formater("Families"))
        self.menu = tk.Menu(self.w)
        self.w.config(menu=self.menu)
        self.menu.add_command(label="Create a new family")
        self.menu.add_command(label="Update", command=self.update)
        self.selectfamily: SelectFamily = SelectFamily(self.w, ui.lang, ui.sql.get_all_families())
        self.selectfamily.w.grid(row=0, column=0, sticky=tk.NSEW, padx=2)
        self.selectfamily.selected_family_id.watch_changes(self.on_change)
        self.frame: ttk.Labelframe | None = None
        pass

    def on_change(self):
        if self.frame != None:
            self.frame.destroy()
        selected_family_id = self.selectfamily.selected_family_id.get()
        assert isinstance(selected_family_id, int)
        self.make_graph(selected_family_id)
        pass

    def make_graph(self, family_id: int):
        self.frame = ttk.Labelframe(self.w, text="Family")
        self.frame.grid(row=1, column=0, padx=2, sticky=tk.NSEW)
        self.canvas = tk.Canvas(self.frame, width=500, height=200)
        family = self.__ui.sql.get_all_families()[family_id]
        self.family: dict[Literal["mom", "dad", "childs"], FamilyPart | ChildPart] = {
            "dad": FamilyPart(self.w, self.__ui, "dad", family.dad, self.act_dad),
            "mom": FamilyPart(self.w, self.__ui, "mom", family.mom, self.act_mom),
            "childs": ChildPart(self.w, self.__ui, family.childs, self.act_childs),
        }
        for family_member_key in self.family.keys():
            family_member = self.family[family_member_key]  # type: ignore
            self.canvas.create_window(coords_for_persons[family_member_key][0], coords_for_persons[family_member_key][1], anchor="w", window=family_member.w)
        self.canvas.create_line(
            coords_for_persons["dad"][0],
            coords_for_persons["dad"][1],
            coords_for_persons["childs"][0] - 50,
            coords_for_persons["dad"][1],
        )
        self.canvas.create_line(
            coords_for_persons["mom"][0],
            coords_for_persons["mom"][1],
            coords_for_persons["childs"][0] - 50,
            coords_for_persons["mom"][1],
        )
        self.canvas.create_line(
            coords_for_persons["childs"][0] - 50,
            coords_for_persons["dad"][1],
            coords_for_persons["childs"][0] - 50,
            coords_for_persons["mom"][1],
        )
        self.canvas.create_line(
            coords_for_persons["childs"][0] - 50,
            coords_for_persons["childs"][1],
            coords_for_persons["childs"][0],
            coords_for_persons["childs"][1],
        )
        self.img = Image.open("./assets/love.png")
        self.img.thumbnail((48, 48))
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(coords_for_persons["childs"][0] - 50, coords_for_persons["childs"][1], image=self.img)  # type: ignore
        # self.canvas.create_image()
        # print(self.family["dad"].w.winfo_reqwidth(), self.family["dad"].w.winfo_reqheight())
        # self.canvas.create_line(0, 0, 10, 10)
        # dad = FamilyPart(self.w, "dad", ui.sql.get_all_families()[0].dad, self.random)
        # test = self.canvas.create_window(50, 50, anchor="nw", window=dad.w)
        self.canvas.grid()

    def act_dad(self, person_id: int):
        print("bonjour")
        self.update()
        pass

    def act_mom(self, person_id: int):
        print("bonjour")
        self.update()
        pass

    def act_childs(self, person_id: int, act: Literal["add", "remove"]):
        if act == "add":
            family = self.__ui.sql.get_all_families()[self.selectfamily.selected_family_id.get()]  # type: ignore
            family.childs.append(self.__ui.sql.get_all_persons()[person_id])
            self.__ui.sql.edit_family(family)
            print("Added someone in the family")
        else:
            print(f"bonjour, {act}, {person_id}")
        self.update()
        pass

    def update(self):
        self.selectfamily.w.destroy()
        self.selectfamily = SelectFamily(self.w, self.__ui.lang, self.__ui.sql.get_all_families())
        self.selectfamily.w.grid(row=0, column=0, sticky=tk.NSEW, padx=2)
        self.selectfamily.selected_family_id.watch_changes(self.on_change)
        if self.frame != None:
            self.frame.destroy()
        self.frame = None


class CreateFamilyWindow:
    def __init__(self, root: tk.Tk, ui: UiTemplate) -> None:
        self.w = tk.Toplevel(root)
        self.box = ttk.Labelframe(self.w)
        self.label = [
            ttk.Label(self.box, text="Dad"),
            ttk.Label(self.box, text="Mom"),
            ttk.Label(self.box, text="Childs"),
        ]
        pass
