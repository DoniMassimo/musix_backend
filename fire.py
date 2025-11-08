import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from chat import Response
import os, json

# firebase_cert_json = os.getenv("FIREBASE_CERT")
# if firebase_cert_json is None:
#     raise ValueError("Cant find env var FIREBASE_CERT")
#
# firebase_cert_dict = json.loads(firebase_cert_json)
# cred = credentials.Certificate(firebase_cert_dict)


def fire_init():
    db_url = os.getenv("FIREBASE_DB_URL")
    if db_url is None:
        raise ValueError("Cant find env var FIREBASE_DB_URL")

    FIRE_CERT = os.getenv("FIREBASE_CERT")
    if FIRE_CERT is None:
        raise ValueError("Cant find env var FIRE_CERT")
    fire_cert_dict = json.loads(FIRE_CERT)
    cred = credentials.Certificate(fire_cert_dict)
    firebase_admin.initialize_app(cred, options={"databaseURL": db_url})


def save_lyric(lyric: Response):
    lyric_dump = lyric.model_dump()

    ref = db.reference("/")
    ref.child("lyrics").child(lyric.lyric.track_id).set(lyric_dump)
