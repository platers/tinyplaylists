from pathlib import Path
from typing import Dict

from tinyplaylists.track import Track


class Playlist:
    name: str
    dir: Path
    tracks: Dict[str, Track]

    def __init__(self, dir: Path):
        self.dir = dir
        self.name = dir.name
        self.load_tracks()

    def load_tracks(self):
        self.tracks = {}
        for file in self.dir.iterdir():
            if file.is_file():
                t = Track.from_file(file)
                self.tracks[t.id] = t
