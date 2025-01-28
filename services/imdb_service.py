import io, time
import requests
import re
from imdb import Cinemagoer
from PIL import Image, ImageTk

class Imdb():
    def __init__(self):
        self.ia = Cinemagoer()

    def clean_filename(self, filename):
        match = re.match(r"^(.*\.(19|20)\d{2})", filename)
        if match:
            # Extract the cleaned part and append the file extension
            cleaned_file = f"{match.group(1)}.{filename.split('.')[-1]}"
            print(cleaned_file)
            return self.search_movie(cleaned_file)
        # Return the original filename if no match
        return self.search_movie(filename)

    def search_movie(self, title):
        try:
            movies = self.ia.search_movie(title)

            if movies:
                movie = movies[0]  # Get the first result
                movie_id = movie.movieID
                movie_details = self.ia.get_movie(movie_id)

                # Check the type of movie_details
                print("Type of movie_details:", type(movie_details))

                # Collect details in a dictionary
                details = {
                    "title": movie_details.get("title", "N/A"),
                    "year": movie_details.get("year", "N/A"),
                    "rating": movie_details.get("rating", "N/A"),
                    "genres": movie_details.get("genres", []),
                    "cast": [person["name"] for person in movie_details.get("cast", [])[:5]],
                    # Get the first 5 cast members
                }

                # Add poster URL if available
                details["cover_url"] = movie_details.get("cover url", "N/A")

                return details
            return None
        except Exception as e:
            print("No matching movies found on IMDb.", e)
            return None

    def receive_posterimg(self, poster_url):
        try:
            response = requests.get(poster_url, timeout=10)
            response.raise_for_status()
            image_data = io.BytesIO(response.content)
            image = Image.open(image_data)
            image = image.resize((450, 450), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print("No image found")
            return None
