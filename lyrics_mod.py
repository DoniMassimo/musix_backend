from syrics.api import Spotify
from typing import Optional, cast
import os


syir: Optional[Spotify] = None


def lyrics_mod_init():
    global syir
    SP_DC = os.getenv("SP_DC")

    if SP_DC is None:
        raise ValueError("Cant find env var SP_DC")

    syir = Spotify(SP_DC)


def download_lyrics(track_id: str) -> dict:
    if syir is None:
        raise RuntimeError("syir not initialized")
    lyrics = syir.get_lyrics(track_id)
    if lyrics is None:
        raise Exception("lyric = None")
    lyrics["lyrics"]["track_id"] = track_id
    return cast(dict, lyrics)
