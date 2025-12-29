import firebase_admin
from firebase_admin import credentials, db
from chat import Response
import os
import json


def fire_init():
    db_url = os.getenv("FIREBASE_DB_URL")
    if db_url is None:
        raise ValueError("Cant find env var FIREBASE_DB_URL")

    FIRE_CERT = os.getenv("FIREBASE_CERT")
    if FIRE_CERT is None:
        raise ValueError("Cant find env var FIREBASE_CERT")
    fire_cert_dict = json.loads(FIRE_CERT)
    cred = credentials.Certificate(fire_cert_dict)
    firebase_admin.initialize_app(cred, options={"databaseURL": db_url})


def transl_exist(transl_id):
    ref = db.reference(f"lyrics/{transl_id}")
    data = ref.get()
    if data:
        return True
    return False


def delete_translation(transl_id):
    ref = db.reference(f"lyrics/{transl_id}")
    ref.delete()


def save_lyric(lyric: Response):
    lyric_dump = lyric.model_dump()

    ref = db.reference("/")
    ref.child("lyrics").child(lyric.lyric.track_id).set(lyric_dump)


def get_all_ids() -> list:
    ref = db.reference("lyrics")
    raw_ids = ref.get(False, True)
    if raw_ids:
        if isinstance(raw_ids, dict):
            return list(raw_ids.keys())
    return []


def get_transl_data(transl_id) -> dict:
    ref = db.reference("lyrics" + "/" + transl_id)
    data = ref.get()
    if isinstance(data, dict):
        return data
    return {}
