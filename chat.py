from openai import OpenAI
from pydantic import BaseModel
import json


class Line(BaseModel):
    start_time_ms: int
    words: str
    trans: str
    comment: str


class Lyric(BaseModel):
    track_id: str
    spoty_api_data: None
    sync_type: str
    lines: list[Line]


Lyric.model_rebuild()


class Response(BaseModel):
    lyric: Lyric


def trans_lyric(lyric: dict) -> Response:
    client = OpenAI()
    lyric_json = json.dumps(lyric)
    response = client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": "Il tuo compito e tradurre dei testi delle canzoni dall'inglese all'italiano. Di verra dato del testo formattato come un json, il tuo compito sara' darmi un risposta in un formato strutturato, dovrai mettare dentro sync_type syncType, detnro start_time_ms startTimeMs, dentro words metti words, poi dovrai effettuare la traduzione linea per linea e metterle dentro trans, infine se neccessario aggiungere anche un comment che spieghi robe magari non chiare nella traduzione, il commento deve essere comunque snello. Metti un dizionario vuoto in sporty_api_data. Nota sulla traduzione: non deve essere letterale o mantenere le metriche, l'importante è che chi legga capisca cosa intende l'artista",
            },
            {"role": "user", "content": lyric_json},
        ],
        text_format=Response,
    )
    translation: Response
    if response.output_parsed:
        translation: Response = response.output_parsed
        return translation
    else:
        raise Exception("trans = None")
