import chat
import lyrics_mod
import fire
import spoty
from flask import Flask, jsonify, request, abort
import threading
from enum import Enum
from dotenv import load_dotenv
import traceback
import os
import logging


load_dotenv("config/secrets.env")
API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise ValueError("Cant find env var API_KEY")
fire.fire_init()
lyrics_mod.lyrics_mod_init()
spoty.spoty_init()


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


class PipelineState(Enum):
    STOP = "stop"
    DOWNLOADING = "downloading"
    TRANSLATING = "translating"
    SAVING = "saving"
    SUCCES = "succes"
    FAILED = "failed"


pipeline_running = False
pipeline_state = PipelineState.STOP


@app.before_request
def check_api_key():
    key = request.headers.get("x-api-key")
    if key != API_KEY or API_KEY is None:
        return jsonify({"msg": "Unauthorized"}), 401


def translation_pipeline(track_id):
    global pipeline_running, pipeline_state
    pipeline_running = True
    try:
        pipeline_state = PipelineState.DOWNLOADING
        lyric = lyrics_mod.download_lyrics(track_id)

        pipeline_state = PipelineState.TRANSLATING
        trans_lyric: chat.Response = chat.trans_lyric(lyric)

        spoty_api_data = spoty.get_track_info(track_id)
        trans_lyric.lyric.spoty_api_data = spoty_api_data

        pipeline_state = PipelineState.SAVING
        fire.save_lyric(trans_lyric)

        pipeline_state = PipelineState.SUCCES
        pipeline_running = False
    except Exception as e:
        print(e)
        traceback.print_exc()
        pipeline_state = PipelineState.FAILED
        pipeline_running = False


@app.route("/get_state")
def get_pipeline_state():
    global pipeline_state
    val = pipeline_state
    if pipeline_state in (PipelineState.FAILED, PipelineState.SUCCES):
        pipeline_state = PipelineState.STOP
    return jsonify({"status": val.value}), 200


@app.route("/add/<track_id>")
def add_track(track_id: str):
    global pipeline_running
    if pipeline_running:
        return jsonify({"status": "busy"}), 429
    thread = threading.Thread(target=translation_pipeline, args=(track_id,))
    thread.start()
    return jsonify({"status": "pipeline started"}), 202


@app.route("/get_tracks_ids")
def get_tracks_ids():
    tracks_ids = fire.get_all_ids()
    return jsonify(tracks_ids), 200


@app.route("/get_track_data/<track_id>")
def get_track_data(track_id: str):
    return fire.get_track_data(track_id)


@app.route("/")
def home():
    logger.info("caiooo")
    return jsonify({"msg": "Hello"}), 200


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
