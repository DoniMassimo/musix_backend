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
    prompt = ResponsePromptParam(
        id="pmpt_6942d50237c081969b659017cdfceec508145f8c56c1e818",
        variables={"song": song, "album": album, "artist": artist},
    )
    response = client.responses.parse(
        model="gpt-5-nano-2025-08-07",
        prompt=prompt,
        input=[
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
