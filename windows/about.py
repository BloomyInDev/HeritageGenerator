import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from components.common import title_formater


class AboutWindow:
    def __init__(self, root_element: tk.Tk) -> None:
        # Create a new window
        self.w = tk.Toplevel(root_element)

        # Load the image and process it
        self.image = Image.open("./assets/icon.ico")
        self.image.thumbnail((128, 128), Image.Resampling.LANCZOS)

        # Settings for the new window
        self.w.resizable(False, False)
        self.w.title(title_formater("About"))
        self.w.bind("<Escape>", lambda event: self.w.destroy())

        # Setup the image displayer
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.image_displayer = ttk.Label(self.w, image=self.tk_image)
        self.image_displayer.grid(row=0, column=0, sticky=tk.EW, padx=(self.image.width - self.w.winfo_width()) / 2)

        # Setup all the rest

        self.name_app = ttk.Label(self.w, text="HeritageGenerator")
        self.name_app.grid(row=1, column=0)
        self.desc = ttk.Label(self.w, text="A simple app to make family tree")
        self.desc.grid(row=2, column=0)
        pass
