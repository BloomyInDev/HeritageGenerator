import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from components.common import title_formater
from utils.config import Language
from utils.person import Person
from utils.ui_template import UiTemplate


class AdditionalFilesManager:
    def __init__(self, root: tk.BaseWidget, lang: Language, person: Person, ui: UiTemplate) -> None:
        self.w = tk.Toplevel(root)
        self.w.title(title_formater(lang.get(["additional-files", "title"]).replace("{person-name}", f"{person.first_name} {person.name}")))
        pass
