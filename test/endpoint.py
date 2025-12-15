import requests
from pprint import pprint

base_url = "http://127.0.0.1:5000"

API_KEY = None


def test__404():
    url = base_url + "/placholder"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    pprint(response.json())


def test__rq_test():
    url = base_url + "/rq"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.ok:
        pprint(response.json())


def test__hello():
    url = base_url + "/"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.ok:
        pprint(response.json())


def test__get_tracks_ids():
    url = base_url + "/get_tracks_ids"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.ok:
        pprint(response.json())


def test__get_track_data(track_id):
    url = base_url + "/get_track_data/" + track_id
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.ok:
        pprint(response.json())


def test__start_transl_job(track_id):
    url = f"{base_url}/start_transl_job/{track_id}"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    pprint(response.json())


def test__get_transl_job_state(job_id):
    url = f"{base_url}/transl_job_state/{job_id}"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    pprint(response.json())
