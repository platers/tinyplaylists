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
