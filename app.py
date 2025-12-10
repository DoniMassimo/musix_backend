import fire
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import logging


load_dotenv("config/secrets.env")
API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise ValueError("Cant find env var API_KEY")
fire.fire_init()


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

fmt = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s")
fh = logging.FileHandler("app.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(fmt)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(fmt)

logger = logging.getLogger(app.name)
logger.addHandler(fh)
logger.addHandler(sh)


@app.before_request
def check_api_key():
    key = request.headers.get("x-api-key")
    if key != API_KEY or API_KEY is None:
        return jsonify({"msg": "Unauthorized"}), 401


@app.route("/get_tracks_ids")
def get_tracks_ids():
    tracks_ids = fire.get_all_ids()
    return jsonify(tracks_ids), 200


@app.route("/get_track_data/<track_id>")
def get_track_data(track_id: str):
    return fire.get_track_data(track_id)


@app.route("/")
def home():
    return jsonify({"msg": "Hello"}), 200


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
