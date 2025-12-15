from openai import OpenAI
from pydantic import BaseModel
import json
from pprint import pprint


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
        model="gpt-5-nano-2025-08-07",
        input=[
            {
                "role": "system",
                "content": """Il tuo compito è spiegare testi inlgesi in italiano in modo da capirne il significato.
                            Di verra dato del testo formattato come un json, il tuo compito sarà darmi un risposta in un formato strutturato, dovrai mettare dentro sync_type syncType, detnro start_time_ms startTimeMs, dentro words metti words, poi dovrai effettuare la spieagazione linea per linea e metterle dentro trans, devi cercare di essere succinto, in lineae generale sarebbe comodo se la spiegazione non superasse 3 volte il numero di caratteri del testo original (spiegazione < 3 * num char testo originale).
                            Infine se neccessario aggiungere in comment cose che non ci stavanao nella spiegazione succinta.
                            Il testo potrebbe contenere ripetzioni, lascia le righe a cui hai gia dato una spiegazione vuote.""",
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
        pprint("risposta: ###############")
        pprint(response)
        raise Exception("trans = None")
