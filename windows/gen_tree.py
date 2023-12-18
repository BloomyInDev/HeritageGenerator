import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror  # type: ignore
from utils.tree import TreeGen
from utils.ui_template import UiTemplate
from components.common import big_btn_formater, title_formater
from windows.preview import PreviewWindow
from windows.select_person import SelectPersonWindow

types_of_trees = {"full": "All persons", "ancestors": "Ancestors of a person", "descendants": "Descendants of a person"}
export_format = {"preview": "Show a preview", "pdf": "Export as a PDF", "png": "Export as a PNG (Image)", "svg": "Export as a SVG"}


class GenTreeWindow:
    def __init__(self, root: tk.Tk, ui: UiTemplate) -> None:
        self.__root = root
        assert isinstance(ui.tree, TreeGen)
        self.tree = ui.tree
        self.__ui = ui
        self.w = tk.Toplevel(root)
        self.w.resizable(False, False)
        self.w.title(title_formater("Generate Tree"))
        self.w.bind("<Escape>", lambda event: self.w.destroy())
        self.w.focus()
        self.frame = ttk.Frame(self.w)
        self.frame.grid(row=0, column=0, pady=5, padx=5)
        self.tree_menu_btn = ttk.Menubutton(self.frame, text="Type of tree")
        self.tree_menu = tk.Menu(self.tree_menu_btn, tearoff=0)
        self.selected_item_tree_menu = tk.StringVar()
        self.selected_item_tree_menu.set("full")
        self.selected_item_tree_menu.trace("w", self.update_selected_tree_menu)  # type: ignore
        for i in range(len(types_of_trees)):
            self.tree_menu.add_radiobutton(label=types_of_trees[list(types_of_trees.keys())[i]], value=list(types_of_trees.keys())[i], variable=self.selected_item_tree_menu)
        self.tree_menu_btn["menu"] = self.tree_menu
        self.tree_menu_btn.grid(row=0, column=0)

        self.format_menu_btn = ttk.Menubutton(self.frame, text="Export format")
        self.format_menu = tk.Menu(self.format_menu_btn, tearoff=0)
        self.selected_item_format_menu = tk.StringVar()
        self.selected_item_format_menu.set("preview")
        self.selected_item_format_menu.trace("w", self.update_selected_tree_menu)  # type: ignore
        for i in range(len(types_of_trees)):
            self.format_menu.add_radiobutton(label=export_format[list(export_format.keys())[i]], value=list(export_format.keys())[i], variable=self.selected_item_format_menu)
        self.format_menu_btn["menu"] = self.format_menu
        self.format_menu_btn.grid(row=1, column=0, columnspan=2, sticky=tk.EW)
        self.person_choosen: int | None = None
        self.choose_person = ttk.Button(self.frame, text="Select a person", command=lambda: SelectPersonWindow(root, self.tree.get_persons(), self.update_selected_person))
        self.choose_person.grid(row=0, column=1)
        self.btn = ttk.Button(self.frame, text=big_btn_formater("Generate !"), command=self.generate_and_display_tree)
        self.btn.grid(row=2, column=0, columnspan=2, sticky=tk.EW)
        self.update_selected_tree_menu()  # type: ignore
        pass

    def update_selected_tree_menu(self, *args):  # type: ignore
        if self.selected_item_tree_menu.get() == "full":
            self.choose_person.configure(state="disabled")
        else:
            self.choose_person.configure(state="normal")
        pass

    def update_selected_person(self, person_id: int):
        self.person_choosen = person_id

    def generate_and_display_tree(self):
        assert isinstance(self.tree, TreeGen)
        person_id = None
        if self.person_choosen == None and self.selected_item_tree_menu.get() != "full":
            showerror(title_formater("Error"), "You need to specify a Person for this tree type")
            return
        else:
            person_id = self.person_choosen
        print(self.selected_item_format_menu.get())
        print(f'Generate "{self.selected_item_tree_menu.get()}" tree {f"for {str(self.tree.get_persons()[self.person_choosen])}" if self.person_choosen != None else ""}')
        if self.selected_item_format_menu.get() == "preview":
            print("In preview mode")
            file_path = self.tree.gen_tree(self.selected_item_tree_menu.get(), person_id, "png", False)  # type: ignore
            PreviewWindow(self.__root, self.__ui, file_path)
        else:
            file_path = self.tree.gen_tree(self.selected_item_tree_menu.get(), person_id, self.selected_item_format_menu.get(), True)  # type: ignore
