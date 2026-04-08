import requests
from syrics.api import Spotify
from typing import Optional, cast
import os
from pprint import pprint
import json

# syir: Optional[Spotify] = None


# def lyrics_mod_init():
#     global syir
#     SP_DC = os.getenv("SP_DC")
#
#     if SP_DC is None:
#         raise ValueError("Cant find env var SP_DC")
#
#     syir = Spotify(SP_DC)


# def download_lyrics_syrics(track_id: str) -> dict:
#     if syir is None:
#         raise RuntimeError("syir not initialized")
#     lyrics = syir.get_lyrics(track_id)
#     if lyrics is None:
#         return {}
#
#     ret = {"lyrics": {}}
#     ret["lyrics"]["syncType"] = lyrics["lyrics"]["syncType"]
#     ret["lyrics"]["lines"] = lyrics["lyrics"]["lines"]
#     ret["lyrics"]["track_id"] = track_id
#
#     return cast(dict, ret)


def _time_to_ms(time_str: str) -> int:
    minutes, rest = time_str.split(":")
    seconds, centiseconds = rest.split(".")
    total_ms = int(minutes) * 60 * 1000 + int(seconds) * 1000 + int(centiseconds) * 10
    return total_ms


def download_lyrics_lrclib(song: str, artist=None, album=None) -> dict:
    url = "http://lrclib.net/api/get"
    params = {"artist_name": artist, "track_name": song, "album_name": album}
    params = {k: v for k, v in params.items() if v is not None}
    response = requests.get(url, params=params, timeout=(30, 60))
    lrclib_res = response.json()

    lines = []
    times = None
    isSynced = lrclib_res["syncedLyrics"] != None

    if isSynced:
        print("s")
        lines = lrclib_res["syncedLyrics"].split("\n")
        times = list(map(lambda line: line.split("]")[0][1:], lines))
        times = list(map(lambda time: _time_to_ms(time), times))
        lines = list(map(lambda line: line.split("]")[1][1:], lines))
        complete_lines = list(
            map(
                lambda xy: {
                    "words": xy[0],
                    "start_time_ms": xy[1],
                    "trans": "",
                    "comment": "",
                },
                zip(lines, times),
            )
        )
    else:
        print("n")
        lines = lrclib_res["plainLyrics"].split("\n")
        complete_lines = list(
            map(
                lambda line: {
                    "words": line,
                    "start_time_ms": 0,
                    "trans": "",
                    "comment": "",
                },
                lines,
            )
        )

    ret = {"lyric": {}}
    ret["lyric"]["syncType"] = "LINE_SYNCED" if isSynced else ""
    ret["lyric"]["lines"] = complete_lines
    pprint(ret)
    return ret
