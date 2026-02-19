import sys
from pathlib import Path
import json
from pprint import pprint
import tasks

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

import spoty
import lyrics_mod
import fire

lyrics_mod.lyrics_mod_init()
spoty.spoty_init()
fire.fire_init()


def generate_download_lyric_mock():
    lyric = lyrics_mod.download_lyrics_syrics("4sJFW6APhXl5v7idGF3QWd")
    with open("mock_file/mock_lyric.json", "w", encoding="utf-8") as file:
        json.dump(lyric, file, ensure_ascii=False, indent=4)


def generate_spoty_track_info_mock():
    track_info = spoty.get_track_info("2EBCVPNAG46nbgs6jXPGvv")
    with open("mock_file/mock_track_info.json", "w", encoding="utf-8") as file:
        json.dump(track_info, file, ensure_ascii=False, indent=4)


def test__download_lyrics_lrclib():
    a = lyrics_mod.download_lyrics_lrclib(song="Walkin", artist="Denzel Curry")
    pprint(a)


def test__pipeline(track_id: str):
    if fire.transl_exist(track_id):
        raise Exception(f"translation with id {track_id} already exists")
    lyric = None
    spoty_api_data = spoty.get_track_info(track_id)
    try:
        lyric = lyrics_mod.download_lyrics_lrclib(
            song=spoty_api_data["name"],
            artist=spoty_api_data["artists"][0]["name"],
            album=spoty_api_data["album"]["name"],
        )
        lyric["lyric"]["track_id"] = track_id
    except:
        raise Exception(f"lyric for {track_id} temporarily unavailable for download")

    if not lyric:
        raise Exception(f"lyric for {track_id} not available for download")
    tasks.translation_pipeline_norq(track_id, lyric)
