import requests
from urllib.parse import urljoin
import os
from dotenv import load_dotenv
from pprint import pprint

base_url = "http://127.0.0.1:5000"
load_dotenv("config/secrets.env")
API_KEY = os.getenv("API_KEY")


def basic_test():
    headers = {"x-api-key": API_KEY}
    url = base_url + "/" + "/get_track_data/" + "01BBYgKvjw5ye99zQTAK7P"
    response = requests.get(url, headers=headers)
    pprint(response.json())


if __name__ == "__main__":
    basic_test()
