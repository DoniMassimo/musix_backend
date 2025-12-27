import fire
from flask import Flask, jsonify, request
import dotenv
import os
import logging
import redis
import rq
from rq.exceptions import NoSuchJobError
import tasks
from pprint import pprint


dotenv.load_dotenv("config/secrets.env")
API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise ValueError("Cant find env var API_KEY")

redis_conn = redis.Redis()
queue = rq.Queue(connection=redis_conn)

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

fmt = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s"
)
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


@app.route("/transl_job_state/<job_id>")
def get_transl_job_state(job_id: str):
    try:
        transl_job = rq.job.Job.fetch(job_id, redis_conn)
    except NoSuchJobError:
        ret = jsonify(
            {
                "succes": False,
                "error": {
                    "code": "RESOURCE_NOT_FOUND",
                    "message": f"translation job not found with id{job_id}",
                },
            }
        )
        return ret, 404
    job_status = transl_job.get_status().value
    job_meta = transl_job.get_meta()
    if job_status in (
        rq.job.JobStatus.FINISHED,
        rq.job.JobStatus.FAILED,
        rq.job.JobStatus.CANCELED,
        rq.job.JobStatus.STOPPED,
    ):
        transl_job.delete()
    return (
        jsonify({"succes": True, "data": {"status": job_status, "meta": job_meta}}),
        200,
    )


@app.route("/start_transl_job/<track_id>", methods=["POST"])
def start_transl_job(track_id: str):
    data = request.get_json(silent=True)
    user_instruction = ""
    if data and "instruction" in data:
        user_instruction = data["instruction"]
    transl_job = queue.enqueue(
        tasks.translation_pipeline, track_id, user_instruction, job_timeout="20m"
    )
    job_id = transl_job.get_id()
    ret = jsonify({"succes": True, "data": {"transl_job_id": job_id}})
    return (ret, 202)


@app.route("/get_tracks_ids")
def get_tracks_ids():
    tracks_ids = fire.get_all_ids()
    return jsonify(tracks_ids), 200


@app.route("/get_track_data/<track_id>")
def get_track_data(track_id: str):
    return fire.get_track_data(track_id)


@app.errorhandler(404)
def handle_404(error):
    return (
        jsonify(
            {
                "success": False,
                "error": {
                    "code": "RESOURCE_NOT_FOUND",
                },
            }
        ),
        404,
    )


@app.route("/")
def home():
    return jsonify({"msg": "Hello"}), 200


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
