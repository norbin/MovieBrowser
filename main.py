import tkinter as tk
from tkinter import ttk
from tkinter import Menu, N, S, E, W, VERTICAL, Text, PhotoImage, Label, Scrollbar

from controllers.menu_controller import MenuController
from controllers.tree_controller import TreeController
from controllers.details_controller import DetailsController

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie Browser")
        self.geometry("1400x800")

        # Create the main frame
        self.main = ttk.Frame(padding=(5, 5, 5, 5))
        self.main.grid(column=0, row=0, sticky=(N, S, E, W))

        # Configure the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=1)

        # Create left frame
        self.left = ttk.Frame(self.main, padding=(5, 5, 5, 5))
        self.left.grid(column=0, row=0, sticky=(N, S, E, W))
        self.left.grid_rowconfigure(0, weight=1)
        self.left.grid_columnconfigure(0, weight=1)

        # Add TreeView to left
        self.tree = ttk.Treeview(self.left, columns=('value'), show='tree')
        self.tree.heading("#0", text="Directories", anchor=W)
        self.tree.grid(row=0, column=0, sticky=(N, S, E, W))

        # Add vertical scrollbar
        scrollbar = Scrollbar(self.left, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=2, sticky=(N, S))

        # Create right frame for Text widget
        self.right = ttk.Frame(self.main, padding=(5, 5, 5, 5))
        self.right.grid(column=1, row=0, sticky=(N, S, E, W))
        self.right.grid_rowconfigure(0, weight=1)
        self.right.grid_columnconfigure(0, weight=1)

        # Add ProgressBar
        self.progress = ttk.Progressbar(self.right, mode="indeterminate")
        self.progress.grid(row=1, column=0, pady=10, sticky="ew")
        self.progress.grid_remove()  # Hide initially

        # Ensure the Text widget is created once in the __init__ method
        self.details_text = Text(self.right, wrap="word", padx=10, pady=10)
        self.details_text.grid(row=0, column=0, sticky=(N, S, E, W))
        self.details_text.insert("1.0", "Select Movie")  # Set default text
        self.details_text.config(state="normal")  # Allow editing or copying

        # Add Poster Display
        self.poster_label = Label(self.right)
        self.poster_label.grid(row=2, column=0, pady=10)
        self.default_image_path = "assets/images/imdb.png"  # Default poster path
        self.default_image = PhotoImage(file=self.default_image_path)  # Load default image
        self.poster_label.config(image=self.default_image)

        # Controller for the right frame
        self.details_controller = DetailsController(
            progress=self.progress,
            details_text=self.details_text,
            poster_label=self.poster_label,
            default_image=self.default_image
        )

        # Controller for the TreeView
        self.tree_controller = TreeController(
            tree=self.tree,
            progress=self.progress,
            update_callback=self.details_controller.handle_update
        )

        # Controller for the Menus
        self.menu_controller = MenuController(self, tree=self.tree)

        self.default_directory = "/media/norbin/VideosandMore/"
        self.tree_controller.populate_tree(self.default_directory)

        # Bind event TreeView clicked
        self.tree.bind("<<TreeviewSelect>>", self.tree_controller.on_tree_select)

        # Add menu
        self.menu = Menu(self, tearoff=0)
        self.config(menu=self.menu)

        # File menu
        self.menu_file = Menu(self.menu, tearoff=0)
        self.menu_file.add_command(label="Open Directory..", command=self.menu_controller.open_directory)
        self.menu.add_cascade(menu=self.menu_file, label="File")

        # Help menu
        self.menu_help = Menu(self.menu, tearoff=0)
        self.menu_help.add_command(label="About", command=self.menu_controller.show_about)
        self.menu.add_cascade(menu=self.menu_help, label="Help")

if __name__ == '__main__':
    app = App()
    app.mainloop()