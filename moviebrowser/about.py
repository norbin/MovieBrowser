from tkinter import Toplevel, Scrollbar
from tkhtmlview import HTMLLabel


class About(Toplevel):
    def __init__(self, parent, html_content):
        super().__init__(parent)
        self.html_content = html_content
        self.title("About")
        self.geometry("600x600")

        #HTML Label to display HTML content
        self.html_label = HTMLLabel(self, html=self.html_content, pady=5, padx=5)
        self.html_label.grid(row=0, column=0, sticky="nsew")

        #Configure
        self.html_label.rowconfigure(0, weight=1)
        self.html_label.columnconfigure(0, weight=1)

        self.scrollbar = Scrollbar(self, command=self.html_label.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.html_label.config(yscrollcommand=self.scrollbar.set)
