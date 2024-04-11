import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import tkinter.filedialog as fdiag
import os
from turtle import width
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
        self.change_pp = PPChangeWindow(self.w, self.__ui, self.lang, self.person)
        return


class PPChangeWindow:
    def __init__(self, root: tk.BaseWidget, ui: UiTemplate, lang: Language, person: Person) -> None:
        self.img_path = fdiag.askopenfilename(filetypes=[("Image", "*.png")])
        if self.img_path == "":
            del self
        else:
            print(self.img_path)
            self.img: Image.Image = Image.open(self.img_path)
            self.img.thumbnail(ui.cfg.get(["images", "resize"]), Image.Resampling.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(self.img)
            self.w = tk.Toplevel(root)
            self.canvas = tk.Canvas(
                self.w,
                width=self.img.width,
                height=self.img.height,
            )
            self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)  # type: ignore
            self.canvas.bind("<Button-1>", self.canvas_click_callback)
            self.canvas.grid(row=0, column=0)
            self.crop_pos = [0, 0]
            self.original_size = (150, 194)
            self.factor = 1
            self.size = [150, 194]
            self.draw_on_canvas()
        pass

    def canvas_click_callback(self, event: Any):
        x, y = event.x, event.y
        # It will always be the case (just for my IDE)
        assert isinstance(x, int)
        assert isinstance(y, int)
        if x + 150 > self.img.width:
            x = self.img.width - 150
        if y + 194 > self.img.height:
            y = self.img.height - 194

        self.crop_pos = [x, y]
        self.draw_on_canvas()

    def draw_on_canvas(self):
        self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)  # type: ignore
        self.canvas.create_rectangle(
            self.crop_pos[0],
            self.crop_pos[1],
            self.crop_pos[0] + (self.original_size[0] * self.factor),
            self.crop_pos[1] + (self.original_size[1] * self.factor),
            width=2,
        )
