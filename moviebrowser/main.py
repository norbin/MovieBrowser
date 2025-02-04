import tkinter as tk
from tkinter import ttk, W, Scrollbar, Text, Label, PhotoImage, Menu
from tkinter.constants import VERTICAL
from controller import Controller


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie Browser")
        self.geometry("1200x800")

        #Create the main frame
        self.main = ttk.Frame(padding=(5, 5, 5, 5))
        self.main.grid(column=0, row=0, sticky="nsew")

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=1)

        # Create left frame
        self.left = ttk.Frame(self.main, padding=(5, 5, 5, 5))
        self.left.grid(column=0, row=0, sticky="nsew")
        self.left.rowconfigure(0, weight=1)
        self.left.columnconfigure(0, weight=1)

        # Add treeview to the left
        self.tree = ttk.Treeview(self.left, columns=("value"), show="tree")
        self.tree.heading("#0", text="Browse directories here", anchor=W)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Add vertical scrollbar
        self.scrollbar = Scrollbar(self.left, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=2, sticky="ns")

        # Create right frame
        self.right = ttk.Frame(self.main, padding=(5, 5, 5, 5))
        self.right.grid(column=1, row=0, sticky="nsew")
        self.right.rowconfigure(0, weight=1)
        self.right.columnconfigure(0, weight=1)

        # Add progressbar
        self.progress = ttk.Progressbar(self.right, mode="indeterminate")
        self.progress.grid(row=1, column=0, pady=10, sticky="ew")
        self.progress.grid_remove()

        # Add the Text widget
        self.details_text = Text(self.right, wrap="word", padx=10, pady=10)
        self.details_text.grid(row=0, column=0, sticky="nsew")
        self.details_text.insert("1.0", "Here you will see Movie Details")
        self.details_text.config(state="normal")

        # Add poster display
        self.poster_label = Label(self.right)
        self.poster_label.grid(row=3, column=0, pady=5)
        self.default_image_path = "assets/images/imdb.png"
        self.default_image = PhotoImage(file=self.default_image_path)
        self.poster_label.config(image=self.default_image)

        # Init the Controller
        self.controller = Controller(
            root=self,
            tree=self.tree,
            progress=self.progress,
            details_text=self.details_text,
            default_image=self.default_image,
            poster_label=self.poster_label
        )

        # Add play button
        self.play_button = ttk.Button(self.right, text="Play Video", command=self.controller.play_movie)
        self.play_button.grid(row=2, column=0, pady=5)

        self.default_dir = "/media/norbin/VideosandMore"
        self.controller.populate_tree(self.default_dir)

        # Bind Event TreeView clicked
        self.tree.bind("<<TreeviewSelect>>", self.controller.tree_entry_select)

        # Add menu
        self.menu = Menu(self, tearoff=0)
        self.config(menu=self.menu)

        # File menu
        self.menu_file = Menu(self.menu, tearoff=0)
        self.menu_file.add_command(label="Open Directory..", command=self.controller.open_directory)
        self.menu.add_cascade(menu=self.menu_file, label="File")

        # Help menu
        self.menu_help = Menu(self.menu, tearoff=0)
        self.menu_help.add_command(label="About", command=self.controller.show_about)
        self.menu.add_cascade(menu=self.menu_help, label="Help")
