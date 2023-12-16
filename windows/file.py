import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import tkinter.filedialog as fdiag
from utils.file import FileLoader
from utils.sql import Sql


def OpenFile(file_loader: FileLoader):
    return file_loader.load(
        fdiag.askopenfilename(
            title="Open a file",
            initialdir="/",
            filetypes=(("HeritageGenerator files", "*.hgb"), ("All files", "*.*")),
        )
    )


def SaveFile(sql_obj: Sql, file_loader: FileLoader):
    return file_loader.save(
        sql_obj,
        fdiag.asksaveasfilename(title="Save a file", initialdir="/", filetypes=(("HeritageGenerator files", "*.hgb"),)),
    )
