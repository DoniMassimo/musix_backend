from flask import Blueprint, abort, jsonify
import fire

data_api = Blueprint("translations", __name__)


@data_api.route("/translations/<string:transl_id>", methods=["DELETE"])
def delete_translation(transl_id: str):
    if not fire.transl_exist(transl_id):
        abort(404, description=f"translation with id {transl_id} does not exisit")
    fire.delete_translation(transl_id)
    ret = jsonify({"succes": True, "data": {"transl_id": transl_id}})
    return (ret, 200)


@data_api.route("/translations_ids")
def get_translations_ids():
    transls_ids = fire.get_all_ids()
    return jsonify(transls_ids), 200


@data_api.route("/translations/<string:transl_id>")
def get_translations(transl_id: str):
    return fire.get_transl_data(transl_id)
