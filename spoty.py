import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from typing import Optional


SPOTIPY_CLIENT_ID: Optional[str] = None
SPOTIPY_CLIENT_SECRET: Optional[str] = None

spoty: Optional[spotipy.Spotify] = None


def spoty_init():
    global spoty
    SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

    if SPOTIPY_CLIENT_ID is None:
        raise ValueError("Cant find env var SPOTIPY_CLIENT_ID")

    if SPOTIPY_CLIENT_SECRET is None:
        raise ValueError("Cant find env var SPOTIPY_CLIENT_SECRET")

    spoty = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri="http://localhost:3000",
            scope="user-library-read",
        )
    )


def get_track_info(track_id: str):
    track_id = "spotify:track:" + track_id
    if spoty is None:
        raise RuntimeError("sp not initialized")
    results = spoty.track(track_id)
    if not results:
        raise Exception("res = None")
    return results
