import threading
from services.tree_view_service import TreeViewService

class TreeController:
    def __init__(self, tree, progress, update_callback):
        self.tree = tree
        self.progress = progress
        self.update_callback = update_callback
        self.tree_view_service = TreeViewService()
    
    def populate_tree(self, parent_path, parent_node=""):
        for entry in self.tree_view_service.list_directory(parent_path):
            entry_path = self.tree_view_service.join(parent_path, entry)
            node = self.tree.insert(parent_node, "end", text=entry, open=False, values=(entry_path,))
            if self.tree_view_service.is_directory(entry_path):
                self.populate_tree(entry_path, node)

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children())

    def on_tree_select(self, event):
        selected_item = self.tree.selection()  # Get selected item IDs
        if selected_item:
            item_id = selected_item[0]  # Extract first selected item's ID
            # Get the item's values
            values = self.tree.item(item_id, "values")
            if values:  # Ensure values exist
                path = values[0]  # Extract the first value (the file path)
                if not self.tree_view_service.is_directory(path):  # Check if it's not a directory
                    print(f"The path is:{path}")
                    filename = self.tree_view_service.get_file_name(path)
                    if self.tree_view_service.is_movie_file(filename):
                        self.fetch_movie_details(filename)
                    else:
                        print("Is not movie File")
                else:
                    print(f"Selected item is a directory: {path}")
            else:
                print(f"Selected item has no associated value: {item_id}")

    def fetch_movie_details(self, filename):
        # Show the progress bar
        self.progress.grid()
        self.progress.start()

        def worker():
            if self.update_callback:
                self.update_callback(filename)

        threading.Thread(target=worker).start()
