import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import tkinter.filedialog as fdiag
import os
from typing import Any
from PIL import Image, ImageTk
from components.common import title_formater
from utils.config import Language
from utils.person import Person
from utils.ui_template import UiTemplate


class AdditionalFilesManagerWindow:
    def __init__(self, root: tk.BaseWidget, lang: Language, person: Person, ui: UiTemplate) -> None:
        self.lang, self.person, self.__ui = lang, person, ui
        self.w = tk.Toplevel(root)
        self.w.title(title_formater(lang.get(["additional-files", "title"]).replace("{person-name}", f"{person.first_name} {person.name}")))
        self.label = ttk.Label(self.w, text=f"{person.first_name} {person.name}")
        self.label.grid(row=0, column=0)
        self.__create_pp_frame()
        self.__create_additional_files_frame()

        pass

    def __create_pp_frame(self):
        self.ppFrame = ttk.Labelframe(self.w, text="Picture")
        self.image_src = f"./temp/cache/{self.person.id}.png" if os.path.isfile(f"./temp/cache/{self.person.id}.png") else "./assets/person.png"
        self.image = Image.open(self.image_src)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.image_displayer = ttk.Label(self.ppFrame, image=self.tk_image)
        self.image_displayer.grid(row=0, column=0, sticky=tk.NSEW)
        self.change_pp_btn = ttk.Button(self.ppFrame, command=self.call_change_pp)
        self.change_pp_btn.grid(row=0, column=10)
        self.ppFrame.grid(row=0, column=1)

    def __create_additional_files_frame(self):
        self.additionalFilesFrame = ttk.Labelframe(self.w, text="Additional files")
        self.additionalFilesFrame.grid(row=0, column=2)

    def call_change_pp(self):
        self.change_pp = PPChangeWindow(self.w, self.lang, self.person)
        return


class PPChangeWindow:
    def __init__(self, root: tk.BaseWidget, lang: Language, person: Person) -> None:
        self.img_path = fdiag.askopenfilename()
        self.w = tk.Toplevel(root)
        self.canvas = tk.Canvas(
            self.w,
            width=600,
            height=400,
        )
        self.canvas.bind("<Button-1>", self.callback)
        self.canvas.grid(row=0, column=0)
        pass

    def callback(self, event: Any):
        print("clicked at", event.x, event.y)
