import sys
from pathlib import Path


parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

import spoty
import lyrics_mod

lyrics_mod.lyrics_mod_init()


def generate_download_lyric_mock():
    lyric = lyrics_mod.download_lyrics("0bYg9bo50gSsH3LtXe2SQn")


def test_openai_smoke():
    pass
