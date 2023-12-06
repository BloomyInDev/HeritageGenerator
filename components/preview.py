import tkinter as tk
import tkinter.ttk as ttk
import os
from PIL import Image, ImageTk
from components.common import title_formater


class PreviewWindow:
    def __init__(self, root_element: tk.Tk, img_path: str) -> None:
        assert os.path.isfile(img_path)

        # Create a new window
        self.w = tk.Toplevel(root_element)

        # Load the image and process it
        self.image = Image.open(img_path)
        max_res = (1152, 648)
        self.image.thumbnail(max_res, Image.Resampling.LANCZOS)

        # Settings for the new window
        self.w.resizable(False, False)
        self.w.geometry(f"{self.image.width+5}x{self.image.height+32}")
        self.w.title(title_formater("Tree preview"))

        # Setup the image displayer
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.image_displayer = ttk.Label(self.w, image=self.tk_image)
        self.image_displayer.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW)

        # Setup others things
        self.txt = ttk.Label(self.w, text="Preview")
        self.txt.grid(row=0, column=0, sticky=tk.W, ipadx=2)
        self.btn = ttk.Button(self.w, text="Close", command=lambda: self.w.destroy())
        self.btn.grid(row=0, column=1, sticky=tk.E, ipadx=2)
        self.sep = ttk.Separator(self.w, orient="horizontal")
        self.sep.grid(row=1, column=0, columnspan=2, sticky=tk.EW)
        pass
