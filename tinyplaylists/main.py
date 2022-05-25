from pathlib import Path
from typing import Dict, Optional
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

    def get_playlist(self, name: str) -> Playlist:
        return self.playlists[name]

    def import_track(self, file: Path, playlist_name: str, metadata: dict) -> Track:
        pl = self.get_playlist(playlist_name)
        return pl.import_track(file, metadata)

    def get_track(self, id: str) -> Optional[Track]:
        for pl in self.playlists.values():
            if id in pl.tracks:
                return pl.tracks[id]
        return None

    def create_playlist(self, name: str) -> Playlist:
        dir = self.root / name
        os.mkdir(dir)
        pl = Playlist(dir)
        self.playlists[name] = pl
        return pl
