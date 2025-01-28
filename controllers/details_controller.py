import threading
from services.imdb_service import Imdb

class DetailsController:
    def __init__(self, progress, details_text, poster_label, default_image):
        self.imdb_service = self.imdb_service = Imdb()
        self.progress = progress
        self.details_text = details_text
        self.poster_label = poster_label
        self.default_image = default_image

    def handle_update(self, filename):
        # Show the progress bar
        self.progress.grid()
        self.progress.start()

        def worker():
            try:
                movie_details = self.imdb_service.clean_filename(filename)

                # Ensure movie_details is a dictionary
                if isinstance(movie_details, dict):
                    self.update_details(movie_details)
                else:
                    print(f"Invalid movie details received: {movie_details}")
                    self.update_details(None)
            except Exception as e:
                print(f"Error fetching movie details: {e}")
                self.update_details(None)
            finally:
                # Hide progress bar in the main thread
                self.progress.stop()
                self.progress.grid_remove()

        threading.Thread(target=worker, daemon=True).start()

    def update_details(self, movie_details):
        if movie_details:
            print(movie_details)
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
            self.update_poster(movie_details['cover_url'])
        else:
            self.details_text.delete("1.0", "end")
            self.details_text.insert("1.0", "No movie details found.")
            self.poster_label.config(image=self.default_image)

    def update_poster(self, poster_url):
        try:
            photo = self.imdb_service.receive_posterimg(poster_url)
            self.poster_label.config(image=photo)
            self.poster_label.image = photo  # Keep reference to avoid garbage collection
        except Exception:
            self.poster_label.config(image=self.default_image)
