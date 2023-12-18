import tkinter as tk
import tkinter.ttk as ttk
import os
from PIL import Image, ImageTk
from components.common import title_formater
from utils.ui_template import UiTemplate


class PreviewWindow:
    def __init__(self, root_element: tk.Tk, ui: UiTemplate, img_path: str) -> None:
        assert os.path.isfile(img_path)

        # Create a new window
        self.w = tk.Toplevel(root_element)

        # Load the image and process it
        self.image = Image.open(img_path)
        max_res = ui.cfg.get(["preview", "window_size"])
        self.image.thumbnail(max_res, Image.Resampling.LANCZOS)

        # Settings for the new window
        self.w.resizable(False, False)
        self.w.geometry(f"{self.image.width}x{self.image.height}")
        self.w.title(title_formater(ui.lang.get(["preview", "title"])))
        self.w.bind("<Escape>", lambda event: self.w.destroy())
        self.w.focus()

        # Setup the Menu
        self.menu = tk.Menu(self.w, tearoff=False)
        self.w.configure(menu=self.menu)
        self.menu.add_command(label="Close", command=lambda: self.w.destroy())

        # Setup the image displayer
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.image_displayer = ttk.Label(self.w, image=self.tk_image)
        self.image_displayer.grid(row=0, column=0, sticky=tk.NSEW)
        pass
