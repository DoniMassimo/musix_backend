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


def test__hello():
    url = base_url + "/"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.ok:
        pprint(response.json())


def test__get_translations_ids():
    url = f"{base_url}/translations_ids"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.ok:
        pprint(response.json())


def test__get_translations(trans_id):
    url = f"{base_url}/translations/{trans_id}"
    headers = {"x-api-key": API_KEY}
    print(headers)
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.ok:
        pprint(response.json())


def test__start_transl_job(trans_id):
    url = f"{base_url}/translations/{trans_id}"
    headers = {"x-api-key": API_KEY}
    http_data = {
        "instruction": "nella sezione comment aggiungi un elenco puntano della parole o modi di dire che per un italinao alle prime armi di inglesee possonorisulare difficili"
    }
    response = requests.post(url, headers=headers, data=http_data)
    print(response.status_code)
    pprint(response.json())


def test__get_transl_job_state(job_id):
    url = f"{base_url}/translations/jobs/{job_id}"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    pprint(response.json())
