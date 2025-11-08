import chat
import lyrics_mod
import fire
import spoty
from flask import Flask, jsonify
import threading
from enum import Enum
from dotenv import load_dotenv
import traceback

app = Flask(__name__)


class PipelineState(Enum):
    STOP = "stop"
    DOWNLOADING = "downloading"
    TRANSLATING = "translating"
    SAVING = "saving"
    SUCCES = "succes"
    FAILED = "failed"


pipeline_running = False
pipeline_state = PipelineState.STOP


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


if __name__ == "__main__":
    load_dotenv("config/secrets.env")
    fire.fire_init()
    lyrics_mod.lyrics_mod_init()
    spoty.spoty_init()
    app.run(debug=True)
