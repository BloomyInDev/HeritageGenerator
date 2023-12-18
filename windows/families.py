import tkinter as tk
import tkinter.ttk as ttk
from typing import Literal
from utils.ui_template import UiTemplate
from components.selector import SelectFamily
from components.family_part import ChildPart, FamilyPart

coords_for_persons: dict[Literal["mom", "dad", "childs", "granddad", "grandmom"], tuple[float, float]] = {
    "dad": (25, 50),
    "mom": (25, 150),
    "childs": (275, 100),
}


class FamiliesWindow:
    def __init__(self, root: tk.Tk, ui: UiTemplate) -> None:
        self.w = tk.Toplevel(root, width=500)
        self.__ui = ui
        self.selectfamily = SelectFamily(self.w, ui.sql.get_all_families())
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
        self.canvas = tk.Canvas(self.frame, width=500)
        family = self.__ui.sql.get_all_families()[family_id]
        self.family: dict[Literal["mom", "dad", "childs", "granddad", "grandmom"], FamilyPart | ChildPart] = {
            "dad": FamilyPart(self.w, self.__ui, "dad", family.dad, self.random),
            "mom": FamilyPart(self.w, self.__ui, "mom", family.mom, self.random),
            "childs": ChildPart(self.w, self.__ui, family.childs, self.random),
        }
        for family_member_key in self.family.keys():
            family_member = self.family[family_member_key]  # type: ignore
            self.canvas.create_window(coords_for_persons[family_member_key][0], coords_for_persons[family_member_key][1], anchor="w", window=family_member.w)

        # dad = FamilyPart(self.w, "dad", ui.sql.get_all_families()[0].dad, self.random)
        # test = self.canvas.create_window(50, 50, anchor="nw", window=dad.w)
        self.canvas.grid()

    def random(self):
        print("bonjour")
        pass
