from pathlib import Path
from typing import Dict
import os

from tinyplaylists.playlist import Playlist


class TinyPlaylists:
    root: Path
    playlists: Dict[str, Playlist]

    def __init__(self, root: Path):
        self.root = root
        self.load_playlists()

    def load_playlists(self):
        self.playlists = {}
        for dir in self.root.iterdir():
            if dir.is_dir():
                self.playlists[dir.name] = Playlist(dir)

    def get_playlist(self, name: str):
        return self.playlists[name]
