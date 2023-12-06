import tkinter as tk
import tkinter.ttk as ttk
from utils.tree import TreeGen
from components.common import big_btn_formater, title_formater
from components.preview import PreviewWindow

types_of_trees = {"full": "All persons", "ancestors": "Ancestors of a person", "descendants": "Descendants of a person"}
export_format = {"preview": "Show a preview", "pdf": "Export as a PDF", "png": "Export as a PNG (Image)", "svg": "Export as a SVG"}


class GenTreeWindow:
    def __init__(self, root: tk.Tk, tree: TreeGen) -> None:
        self.__root = root
        self.tree = tree
        self.w = tk.Toplevel(root)
        self.w.resizable(False, False)
        self.w.title(title_formater("Generate Tree"))
        self.tree_menu_btn = ttk.Menubutton(self.w, text="Type of tree")
        self.tree_menu = tk.Menu(self.tree_menu_btn, tearoff=0)
        self.selected_item_tree_menu = tk.StringVar()
        self.selected_item_tree_menu.set("full")
        self.selected_item_tree_menu.trace("w", self.update_selected_tree_menu)  # type: ignore
        for i in range(len(types_of_trees)):
            self.tree_menu.add_radiobutton(label=types_of_trees[list(types_of_trees.keys())[i]], value=list(types_of_trees.keys())[i], variable=self.selected_item_tree_menu)
        self.tree_menu_btn["menu"] = self.tree_menu
        self.tree_menu_btn.grid(row=0, column=0)

        self.format_menu_btn = ttk.Menubutton(self.w, text="Export format")
        self.format_menu = tk.Menu(self.format_menu_btn, tearoff=0)
        self.selected_item_format_menu = tk.StringVar()
        self.selected_item_format_menu.set("preview")
        self.selected_item_format_menu.trace("w", self.update_selected_tree_menu)  # type: ignore
        for i in range(len(types_of_trees)):
            self.format_menu.add_radiobutton(label=export_format[list(export_format.keys())[i]], value=list(export_format.keys())[i], variable=self.selected_item_format_menu)
        self.format_menu_btn["menu"] = self.format_menu
        self.format_menu_btn.grid(row=1, column=0, columnspan=2, sticky=tk.EW)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self.w, textvariable=self.entry_var)
        self.entry.grid(row=0, column=1)
        self.btn = ttk.Button(self.w, text=big_btn_formater("Generate !"), command=self.generate_and_display_tree)
        self.btn.grid(row=2, column=0, columnspan=2, sticky=tk.EW)
        pass

    def update_selected_tree_menu(self, *args):  # type: ignore
        if self.selected_item_tree_menu.get() == "full":
            self.entry.configure(state="readonly")
        else:
            self.entry.configure(state="normal")

    def generate_and_display_tree(self):
        person_id = None
        if self.entry_var.get().isnumeric():
            person_id = int(self.entry_var.get())
        print(self.selected_item_format_menu.get())
        if self.selected_item_format_menu.get() == "preview":
            print("In preview mode")
            file_path = self.tree.gen_tree(self.selected_item_tree_menu.get(), person_id, "png", False)  # type: ignore
            if file_path != None:
                PreviewWindow(self.__root, file_path)
        else:
            file_path = self.tree.gen_tree(self.selected_item_tree_menu.get(), person_id, self.selected_item_format_menu.get(), True)  # type: ignore
