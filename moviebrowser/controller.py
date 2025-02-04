import os.path
import subprocess
import threading
import markdown2
from service import ControllerService
from service import ImdbService
from tkinter import filedialog
from about import About


class Controller:
    def __init__(self, root, tree, progress, details_text, default_image, poster_label):
        self.root = root
        self.tree = tree
        self.progress = progress
        self.details_text = details_text
        self.default_image = default_image
        self.poster_label = poster_label
        self.controller_service = ControllerService()
        self.selected_movie = None
        self.imdb_service = ImdbService(self.default_image)
        self.about_view = None

    def play_movie(self):
        if self.selected_movie:
            print(f"Playing video: {self.selected_movie}")
            # Use xdg-open to play the video with the default media player
            subprocess.run(["xdg-open", self.selected_movie])
        else:
            print("No filename available to play.")

    def populate_tree(self, parent_path, parent_node=""):
        for entry in self.controller_service.list_directory(parent_path):
            entry_path = self.controller_service.join(parent_path, entry)
            node = self.tree.insert(parent_node, "end", text=entry, open=False, values=(entry_path,))
            if self.controller_service.is_directory(entry_path):
                self.populate_tree(entry_path, node)

    def tree_entry_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]
            values = self.tree.item(item_id, "values")
            if values:
                path = values[0]
                if not self.controller_service.is_directory(path):
                    filename = self.controller_service.get_filename(path)
                    if self.controller_service.is_movie_file(filename):
                        self.selected_movie = path
                        # Start fetch_movie_details in a Thread
                        threading.Thread(target=self.fetch_movie_details, args=(filename,), daemon=True).start()
                    else:
                        self.populate_not_movie_file()

    def fetch_movie_details(self, filename):
        self.progress.grid()
        self.progress.start()
        cleaned_filename = self.imdb_service.clean_filename(filename)
        movie_details = self.imdb_service.search_movie(cleaned_filename)
        #Ensure UI updates run in the main thread
        self.tree.after(0, lambda: self.update_ui_after_fetch(movie_details))

    def update_ui_after_fetch(self, movie_details):
        self.progress.stop()
        self.progress.grid_remove()

        if movie_details:
            self.populate_movie_details(movie_details)
        else:
            self.populate_no_details_found()

    def populate_movie_details(self, movie_details):
        formatted_text = (
            f"Title: {movie_details['title']}\n"
            f"Year: {movie_details['year']}\n"
            f"Rating: {movie_details['rating']}\n"
            f"Genres: {', '.join(movie_details['genres'])}\n"
            f"Cast: {', '.join(movie_details['cast'])}\n"
            f"Poster URL: {movie_details['cover_url']}"
        )
        self.details_text.delete("1.0", "end")
        self.details_text.insert("1.0", formatted_text)
        self.update_poster(movie_details["cover_url"])

    def populate_no_details_found(self):
        self.details_text.delete("1.0", "end")
        self.details_text.insert("1.0", "No movie details found on IMDB")

    def populate_not_movie_file(self):
        self.details_text.delete("1.0", "end")
        self.details_text.insert("1.0", "Not a movie file")

    def update_poster(self, poster_url):
        try:
            photo = self.imdb_service.receive_poster_img(poster_url)
            print(f"photo:{photo}")
            if photo:
                self.poster_label.config(image=photo)
                self.poster_label.image = photo
            else:
                raise ValueError("No image received")
        except Exception as e:
            self.poster_label.config(image=self.default_image)
            self.poster_label.image = self.default_image

    def open_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.clear_tree()
            self.populate_tree(dir_path)

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children())

    def show_about(self):
        readme_path = "README.md"
        content = "README.md not found"
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as file:
                content = file.read()

        if not self.about_view or not self.about_view.winfo_exists():
            html_content = markdown2.markdown(content)
            self.about_view = About(self.root, html_content)
