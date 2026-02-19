from enum import Enum
import chat
import lyrics_mod
import fire
import spoty
import traceback
import rq
import dotenv

dotenv.load_dotenv("config/secrets.env")
fire.fire_init()
lyrics_mod.lyrics_mod_init()
spoty.spoty_init()


class PipelineState(Enum):
    TRANSLATING = "translating"
    SAVING = "saving"
    SUCCES = "succes"


def translation_pipeline(track_id, lyric, user_instruction=""):
    job = rq.get_current_job()
    if job is None:
        raise RuntimeError("No RQ job is currently running")
    try:
        job.meta["state"] = PipelineState.TRANSLATING.value
        job.save_meta()

        spoty_api_data = spoty.get_track_info(track_id)
        trans_lyric: chat.Response = chat.trans_lyric(
            lyric=lyric,
            artist=spoty_api_data["artists"][0]["name"],
            song=spoty_api_data["name"],
            album=spoty_api_data["album"]["name"],
            user_instruction=user_instruction,
        )
        trans_lyric.lyric.spoty_api_data = spoty_api_data

        job.meta["state"] = PipelineState.SAVING.value
        job.save_meta()
        fire.save_lyric(trans_lyric)

        job.meta["state"] = PipelineState.SUCCES.value
        job.save_meta()
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise


def translation_pipeline_norq(track_id, lyric, user_instruction=""):
    try:
        print("translating")

        spoty_api_data = spoty.get_track_info(track_id)
        trans_lyric: chat.Response = chat.trans_lyric(
            lyric=lyric,
            artist=spoty_api_data["artists"][0]["name"],
            song=spoty_api_data["name"],
            album=spoty_api_data["album"]["name"],
            user_instruction=user_instruction,
        )
        trans_lyric.lyric.spoty_api_data = spoty_api_data

        print("saving")
        fire.save_lyric(trans_lyric)

        print("succes")
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise
