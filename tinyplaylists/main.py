from pathlib import Path
from typing import Dict
import os

from tinyplaylists.playlist import Playlist
from tinyplaylists.track import Track


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

    def import_track(self, file: Path, playlist_name: str, metadata: dict) -> Track:
        pl = self.get_playlist(playlist_name)
        return pl.import_track(file, metadata)
