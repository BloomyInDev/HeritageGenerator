import tkinter as tk
from tkinter import ttk, filedialog as fdiag
import os
from typing import Any, Callable, Literal
from PIL import Image, ImageTk
from components.common import title_formater
from components.files import PersonDataFileList
from utils.config import Language
from utils.file import FileInDb
from utils.images import ProfilePicture
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
        self.image_src = (
            f"./temp/file/cache/pp/{self.person.id}{self.person.first_name.lower()}.png"
            if os.path.isfile(f"./temp/file/cache/pp/{self.person.id}{self.person.first_name.lower()}.png")
            else "./assets/person.png"
        )
        self.image = Image.open(self.image_src)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.image_displayer = ttk.Label(self.ppFrame, image=self.tk_image)
        self.image_displayer.grid(row=0, column=0, sticky=tk.NSEW)
        self.change_pp_btn = ttk.Button(self.ppFrame, text="Change", command=self.call_change_pp)
        self.change_pp_btn.grid(row=1, column=0, sticky=tk.EW)
        self.ppFrame.grid(row=1, column=0)

    def __create_additional_files_frame(self):
        self.additionalFilesFrame = ttk.Labelframe(self.w, text="Additional files")
        self.addFilesComponent = PersonDataFileList(self.additionalFilesFrame, self.__ui, self.__ui.sql.get_files_for_person(self.person.id), self.call_change_file)
        self.addFilesComponent.w.grid(row=0, column=0)
        self.additionalFilesFrame.grid(row=2, column=0)

    def call_change_pp(self):
        self.change_pp = PPChangeWindow(self.w, self.__ui, self.lang, self.person, self.update_data)
        return

    def call_change_file(self, f: FileInDb, act: Literal["add", "remove"]):
        print(act, f.id, f.name)
        return

    def update_data(self):
        self.ppFrame.destroy()
        self.additionalFilesFrame.destroy()
        self.__create_pp_frame()
        self.__create_additional_files_frame()


class PPChangeWindow:
    def __init__(self, root: tk.BaseWidget, ui: UiTemplate, lang: Language, person: Person, done_callback: Callable[[], None]) -> None:
        self.lang = lang
        self.__ui = ui
        self.person = person
        self.callback = done_callback
        self.img_path = fdiag.askopenfilename(filetypes=[("Image", "*.png")])
        if self.img_path == "":
            del self
        else:
            self.original_size = (150, 194)
            self.img: Image.Image = Image.open(self.img_path)
            self.img.thumbnail(ui.cfg.get(["images", "resize"]), Image.Resampling.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(self.img)
            self.w = tk.Toplevel(root)
            self.canvas = tk.Canvas(
                self.w,
                width=self.img.width - 1,
                height=self.img.height - 1,
            )
            self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)  # type: ignore
            self.canvas.bind("<Button-1>", self.canvas_click_callback)
            self.canvas.grid(row=0, column=0)

            self.crop_pos = [0, 0]
            self.factor = 1

            self.size = [0, 0]
            self.tk_slider_value = tk.DoubleVar()
            self.slider = ttk.Scale(self.w, from_=1, to=self.calculate_max_factor(), orient="horizontal", variable=self.tk_slider_value, command=self.slider_callback)
            self.slider.grid(row=1, column=0, sticky=tk.EW)
            self.validate_btn = ttk.Button(self.w, text="Valider", command=self.validate_btn_callback)
            self.validate_btn.grid(row=2, column=0, sticky=tk.EW)
            self.calculate_size_with_factor()
            self.draw_on_canvas()
        pass

    def calculate_max_factor(self):
        max_x = self.img.width
        max_y = self.img.height
        x = self.original_size[0]
        y = self.original_size[1]
        if max_x / x < max_y / y:
            return max_x / x
        else:
            return max_y / y

    def canvas_click_callback(self, event: Any):
        x, y = event.x, event.y
        # It will always be the case (just for my IDE)
        assert isinstance(x, int)
        assert isinstance(y, int)
        if x + self.size[0] > self.img.width:
            x = self.img.width - self.size[0]
        if y + self.size[1] > self.img.height:
            y = self.img.height - self.size[1]

        self.crop_pos = [x, y]
        self.draw_on_canvas()

    def calculate_size_with_factor(self):

        future_size = [self.original_size[0] * self.factor, self.original_size[1] * self.factor]
        if round(self.crop_pos[0] + future_size[0]) > self.img.width:
            self.crop_pos[0] = round(self.img.width - future_size[0])
        if round(self.crop_pos[1] + future_size[1]) > self.img.height:
            self.crop_pos[1] = round(self.img.width - future_size[1])
        self.size = future_size

    def draw_on_canvas(self):
        self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)  # type: ignore
        self.canvas.create_rectangle(
            self.crop_pos[0] + 1,
            self.crop_pos[1],
            self.crop_pos[0] + self.size[0],
            self.crop_pos[1] + self.size[1],
            width=2,
        )

    def slider_callback(self, event: Any):
        self.factor = self.tk_slider_value.get()
        self.calculate_size_with_factor()
        self.draw_on_canvas()

    def validate_btn_callback(self):
        ProfilePicture(
            self.img.crop((round(self.crop_pos[0]), round(self.crop_pos[1]), round(self.crop_pos[0] + self.size[0]), round(self.crop_pos[1] + self.size[1]))), self.person, True
        ).save()
        self.w.destroy()
        self.callback()
        del self
