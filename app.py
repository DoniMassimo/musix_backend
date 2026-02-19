import fire
from flask import Flask, abort, jsonify, request
from werkzeug.exceptions import HTTPException
import dotenv
import os
import logging

dotenv.load_dotenv("config/secrets.env")
API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise ValueError("Cant find env var API_KEY")

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

fire.fire_init()


@app.before_request
def check_api_key():
    key = request.headers.get("x-api-key")
    if key != API_KEY or API_KEY is None:
        return jsonify({"msg": "Unauthorized"}), 401


@app.route("/translations/<string:transl_id>", methods=["DELETE"])
def delete_translation(transl_id: str):
    if not fire.transl_exist(transl_id):
        abort(404, description=f"translation with id {transl_id} does not exisit")
    fire.delete_translation(transl_id)
    ret = jsonify({"succes": True, "data": {"transl_id": transl_id}})
    return (ret, 200)


@app.route("/translations_ids")
def get_translations_ids():
    transls_ids = fire.get_all_ids()
    return jsonify(transls_ids), 200


@app.route("/translations/<string:transl_id>")
def get_translations(transl_id: str):
    return fire.get_transl_data(transl_id)


@app.errorhandler(HTTPException)
def handle_http_exception(error):
    response = {
        "success": False,
        "error": {
            "code": error.code,
            "name": error.name,
            "message": error.description,
        },
    }
    return jsonify(response), error.code


@app.route("/")
def home():
    return jsonify({"msg": "Hello"}), 200


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
