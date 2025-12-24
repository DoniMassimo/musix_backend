import sys
from pathlib import Path
import json


parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

import spoty
import lyrics_mod

lyrics_mod.lyrics_mod_init()
spoty.spoty_init()


def generate_download_lyric_mock():
    lyric = lyrics_mod.download_lyrics("57Z6TJCTMACXxdrcwZ3Zvf")
    with open("mock_file/mock_lyric.json", "w", encoding="utf-8") as file:
        json.dump(lyric, file, ensure_ascii=False, indent=4)


def generate_spoty_track_info_mock():
    track_info = spoty.get_track_info("57Z6TJCTMACXxdrcwZ3Zvf")
    with open("mock_file/mock_track_info.json", "w", encoding="utf-8") as file:
        json.dump(track_info, file, ensure_ascii=False, indent=4)
