import io
import os
import re
import requests
from tkinter import Image
from PIL import Image, ImageTk

from imdb import Cinemagoer
from pathlib import Path

class ControllerService:
    def __init__(self):
        self.a = False

    def list_directory(self, parent_path):
        return os.listdir(parent_path)

    def join(self, parent_path, entry):
        return os.path.join(parent_path, entry)

    def is_directory(self, entry_path):
        return os.path.isdir(entry_path)

    def get_filename(self, path):
        return os.path.basename(path)

    def is_movie_file(self, filename):
        extensions = {'.mkv', '.avi', '.mp4', '.mov', '.wmv', '.flv', '.mpeg', '.flac', '.ISO'}
        return Path(filename).suffix in extensions

class ImdbService:
    def __init__(self, default_image):
        self.cinemagoer = Cinemagoer()
        self.default_image = default_image

    def clean_filename(self, filename):
        match = re.match(r"^(.*\.(19|20\d{2}))", filename)
        if match:
            cleaned_filename = f"{match.group(1)}, {filename.split('.')[-1]}"
            return cleaned_filename
        return filename

    def search_movie(self, filename):
        try:
            movies = self.cinemagoer.search_movie(filename)

            if movies:
                movie = movies[0]
                movie_id = movie.movieID
                movie_details = self.cinemagoer.get_movie(movie_id)
                print(movie_details.get("full-size cover url"))
                details = {
                    "title": movie_details.get("title", "N/A"),
                    "year": movie_details.get("year", "N/A"),
                    "rating": movie_details.get("rating", "N/A"),
                    "genres": movie_details.get("genres", []),
                    "cast": [person["name"] for person in movie_details.get("cast", [])],
                }
                details["cover_url"] = movie_details.get("full-size cover url", "N/A")
                return details
            return None
        except Exception as e:
            print("Not found details", e)
        return None

    def receive_poster_img(self, poster_url):
        try:
            response = requests.get(poster_url, timeout=10)
            response.raise_for_status()
            image_data = io.BytesIO(response.content)
            image = Image.open(image_data)
            image = image.resize((550, 550), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print("No image found")
            return self.default_image