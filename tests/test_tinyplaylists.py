import os
from pathlib import Path
import re
import shutil
import pytest
from tinyplaylists.main import TinyPlaylists


@pytest.fixture
def empty_library():
    os.mkdir("test_lib")
    yield Path("test_lib")
    shutil.rmtree("test_lib")


def test_empty_library(empty_library):
    tpl = TinyPlaylists(empty_library)
    assert len(tpl.playlists) == 0


@pytest.fixture
def dir_with_playlists(empty_library):
    os.mkdir("test_lib/playlist1")
    os.mkdir("test_lib/playlist2")

    shutil.copy("tests/audiofiles/2-seconds.mp3", "test_lib/playlist1/a.mp3")
    shutil.copy("tests/audiofiles/2-seconds.mp3", "test_lib/playlist1/b.mp3")

    yield empty_library

    shutil.rmtree("test_lib/playlist1")
    shutil.rmtree("test_lib/playlist2")


@pytest.fixture
def library_with_playlists(dir_with_playlists):
    return TinyPlaylists(dir_with_playlists)


def test_library_with_playlists(library_with_playlists):
    tpl = library_with_playlists
    assert len(tpl.playlists) == 2
    assert "playlist1" in tpl.playlists
    assert "playlist2" in tpl.playlists
    pl1 = tpl.get_playlist("playlist1")
    assert pl1.name == "playlist1"
    assert len(pl1.tracks) == 2


def test_uuid_added_to_file_name(library_with_playlists):
    valid_file_name = re.compile(r"^.*-([0-9a-f]{32}).*$")
    for file in os.listdir("test_lib/playlist1"):
        assert valid_file_name.match(file)


@pytest.fixture
def add_track_to_playlist(library_with_playlists):
    shutil.copy("tests/audiofiles/2-seconds.mp3", "tests/audiofiles/c.mp3")
    tpl = library_with_playlists
    yield tpl.import_track(Path("tests/audiofiles/c.mp3"), "playlist2", {"title": "c"})
    os.remove("tests/audiofiles/c.mp3")


def test_add_track_to_playlist(add_track_to_playlist):
    tpl = TinyPlaylists(Path("test_lib"))
    pl2 = tpl.get_playlist("playlist2")
    assert len(pl2.tracks) == 1
    t = add_track_to_playlist
    assert t.title == "c"
    assert tpl.get_track(t.id) == t


def test_metadata_added(add_track_to_playlist):
    id = add_track_to_playlist.id

    tpl = TinyPlaylists(Path("test_lib"))
    pl2 = tpl.get_playlist("playlist2")
    t = pl2.tracks[id]
    assert t.title == "c"


def test_create_playlist(library_with_playlists):
    tpl = library_with_playlists
    pl3 = tpl.create_playlist("playlist3")
    assert len(tpl.playlists) == 3
    assert pl3.name == "playlist3"
    assert len(pl3.tracks) == 0
    assert pl3.dir == tpl.root / "playlist3"
    assert pl3.dir.exists()


def test_remove_track(add_track_to_playlist):
    tpl = TinyPlaylists(Path("test_lib"))
    id = add_track_to_playlist.id
    tpl.remove_track(id)

    pl2 = tpl.get_playlist("playlist2")
    assert id not in pl2.tracks
    assert not add_track_to_playlist.path.exists()


def test_playlist_tracks(library_with_playlists):
    tpl = library_with_playlists
    tracks = tpl.playlist_tracks("playlist1")
    assert len(tracks) == 2
    values = list(tracks.values())
    assert values[0].title == "a"
    assert values[1].title == "b"
