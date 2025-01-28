import os
import markdown2
from views.about import About
from tkinter import filedialog

class MenuController:
    def __init__(self, root, tree):
        self.root = root
        self.tree = tree
        self.about_view = None

    def open_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.clear_tree()  # Clear the TreeView
            self.populate_tree(dir_path)  # Populate with new directory

    def populate_tree(self, parent_path, parent_node=""):
        for entry in os.listdir(parent_path):
            entry_path = os.path.join(parent_path, entry)
            node = self.tree.insert(parent_node, "end", text=entry, open=False, values=(entry_path,))
            if os.path.isdir(entry_path):
                self.populate_tree(entry_path, node)

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children())

    def show_about(self):
        # Read and display the README.md content
        readme_path = "README.md"
        content = "README.md not found."

        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as file:
                content = file.read()

        if not self.about_view or not self.about_view.winfo_exists():
            html_content = markdown2.markdown(content)
            self.about_view = About(self.root,  html_content)
