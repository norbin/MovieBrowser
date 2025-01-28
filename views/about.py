from tkinter import Toplevel, Scrollbar, N, S, E, W
from tkhtmlview import HTMLLabel

class About(Toplevel):
    def __init__(self, parent, html_content):
        super().__init__(parent) # Initialize Toplevel with parent
        self.html_content = html_content
        self.title = "About"
        self.geometry("600x400")

        # HTMLLabel to display HTML content
        self.html_label = HTMLLabel(self, html=self.html_content, padx=5, pady=5)
        self.html_label.grid(row=0, column=0, sticky=(N, S, E, W))

        # Configure the grid to make the HTMLLabel expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.scrollbar = Scrollbar(self, command=self.html_label.yview)
        self.scrollbar.grid(row=0, column=1, sticky=(N, S))
        self.html_label.config(yscrollcommand=self.scrollbar.set)
