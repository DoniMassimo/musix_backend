import requests
from dotenv import load_dotenv
import os
from pprint import pprint

base_url = "http://127.0.0.1:5000"

API_KEY = None


def test__get_tracks_ids():
    url = base_url + "/get_tracks_ids"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.ok:
        pprint(response.json())


def test__get_track_data():
    track_id = "40Mtjy3zM79tBYMy1R4GLy"
    url = base_url + "/get_track_data/" + track_id
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.ok:
        pprint(response.json())


def test__add_track():
    track_id = "40Mtjy3zM79tBYMy1R4GLy"
    url = base_url + "/add/" + track_id
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.ok:
        pprint(response.json())


def test__get_pipeline_state():
    url = base_url + "/get_state"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.ok:
        pprint(response.json())


if __name__ == "__main__":
    load_dotenv("config/secrets.env")
    API_KEY = os.getenv("API_KEY")
    if API_KEY is None:
        raise ValueError("Cant find env var API_KEY")
    # test__get_tracks_ids()
    test__get_track_data()
    # test__add_track()
    # test__get_pipeline_state()
