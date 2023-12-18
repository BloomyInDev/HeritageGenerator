import tkinter.messagebox as msgbox
import tkinter.filedialog as fdiag
from utils.file import FileLoader
from components.common import title_formater
from utils.ui_template import UiTemplate


def OpenFile(ui: UiTemplate, file_loader: FileLoader):
    return file_loader.load(
        fdiag.askopenfilename(
            title=title_formater(ui.lang.get(["diag", "open", "title"])),
            initialdir="/",
            filetypes=((ui.lang.get(["files", "hgb-files"]), "*.hgb"), (ui.lang.get(["files", "all-files"]), "*.*")),
        )
    )


def SaveFile(ui: UiTemplate, file_loader: FileLoader):
    filepath = fdiag.asksaveasfilename(title=title_formater(ui.lang.get(["diag", "save", "title"])), initialdir="/", filetypes=((ui.lang.get(["files", "hgb-files"]), "*.hgb"),))
    if filepath != "":
        return file_loader.save(
            ui.sql,
            file_path=filepath,
        )
    else:
        return False


def CloseApp(ui: UiTemplate, file_loader: FileLoader):
    if file_loader.file_loaded:
        choice = msgbox.askyesnocancel(title=title_formater(ui.lang.get(["diag", "close", "title"])), message=ui.lang.get(["diag", "close", "msg"]))  # type: ignore
        if choice == True:
            return SaveFile(ui, file_loader)
        elif choice == False:
            return True
        else:
            return False
    else:
        return True
