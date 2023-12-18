import tkinter as tk
from utils.sql import Sql
from utils.file import FileLoader
from utils.tree import TreeGen
from utils.config import Config, Language


class UiTemplate:
    def __init__(self) -> None:
        self.sql: Sql
        self.file_loader: FileLoader
        self.tree: TreeGen | None
        self.cfg: Config
        self.lang: Language
        self.w: tk.Tk
        pass
