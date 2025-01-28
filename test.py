import tkinter as tk
from tkinter import ttk

class MyApp:
    def __init__(self, root):
        # Create TreeView with a single column 'value'
        self.tree = ttk.Treeview(root, columns=('value',), show='headings')
        self.tree.heading('value', text='Value')
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.pack()

        # Insert sample data
        values = ["Value1", "Value2", "Value3"]
        for value in values:
            self.tree.insert("", "end", values=(value,))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()  # Get selected item IDs
        if selected_item:
            item_id = selected_item[0]  # Extract first selected item's ID
            # Get the item's values
            values = self.tree.item(item_id, "values")
            if values:  # Check if values exist
                value = values[0]
                print(f"Selected value: {value}")
            else:
                print(f"Selected item has no associated value: {item_id}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()