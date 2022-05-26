[![Documentation Status](https://readthedocs.org/projects/tinyplaylists/badge/?version=latest)](https://tinyplaylists.readthedocs.io/en/latest/?badge=latest) [![PyTest](https://github.com/platers/tinyplaylists/actions/workflows/actions.yml/badge.svg)](https://github.com/platers/tinyplaylists/actions/workflows/actions.yml) [![PyPI version](https://badge.fury.io/py/tinyplaylists.svg)](https://badge.fury.io/py/tinyplaylists)

# tinyplaylists

A tiny library to organize audio files.

[Documentation](https://tinyplaylists.readthedocs.io/)

## Library Structure

tinyplaylists assumes the obvious folder structure for playlists. Each playlist is a folder that contains the audio files in the playlist.

The name of a playlist is the name of the folder.

Each track is assigned a UUID. A tracks file name ends with the UUID.

An example library is shown below.

```
/
  playlist1
    track1-c0f1803c8a224f34b60b413fa0ee506d.mp3
    track2-032b8f8f8ta3na83a38a3ta893a32o19.mp3
  playlist2
    track3-tn210tn1nt38120tn312031n0t3810nt.mp3
```

Track metadata is stored in the audio file.

## Installation

```
pip install tinyplaylists
```
