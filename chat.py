from openai import OpenAI
from openai.types.responses import ResponsePromptParam
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


def trans_lyric(
    lyric: dict, song="", album="", artist="", user_instruction=""
) -> Response:
    client = OpenAI()
    lyric_json = json.dumps(lyric)

    with open("prompts/test1", "r", encoding="utf-8") as file:
        prompt = file.read()

    response = client.responses.parse(
        model="gpt-5-nano-2025-08-07",
        input=[
            {
                "role": "system",
                "content": (
                    "Le seguenti indicazione che ti vengono date riguardano una canzone con queste informazioni, se le info mancano cerca comunque di portare a termine il compito:"
                    f"- canzone: {song}"
                    f"- artista: {artist}"
                    f"- album: {album}"
                ),
            },
            {
                "role": "system",
                "content": prompt,
            },
            {"role": "user", "content": user_instruction},
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
