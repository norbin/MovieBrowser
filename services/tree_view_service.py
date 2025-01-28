import os
from pathlib import Path

class TreeViewService:
    def __init__(self):
        pass

    def list_directory(self, path):
        return os.listdir(path)

    def is_directory(self, path):
        return os.path.isdir(path)

    def join(self, parent_path, entry):
        return os.path.join(parent_path, entry)

    def get_file_name(self, path):
        return os.path.basename(path)

    def is_movie_file(self, filename):
        extensions = {'.mkv', '.avi', '.mp4', '.mov', '.wmv', '.flv', '.mpeg', '.flac', '.ISO'}
        return Path(filename).suffix in extensions
