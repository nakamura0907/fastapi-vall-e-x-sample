import re
from typing import Union, Tuple
from gradio_client import Client

from .exceptions import DetectedTextNotFoundException
from .schemas import Language, Accent


client = Client("https://plachta-vall-e-x.hf.space/")


def make_prompt(prompt_name: str, file_location: str, transcript: Union[str, None]) -> Tuple[str, str]:
    if transcript is None:
        transcript = ""

    result = client.predict(
        prompt_name,
        file_location,	
        file_location,
        transcript,
        fn_index=3
    )

    # Parse prompt result
    match = re.search(r'\[([^]]+)\](.*?)\[[^]]+\]', result[0])
    if match:
        detected_text = match.group(2)
        return detected_text, result[1]
    else:
        raise DetectedTextNotFoundException()
    
def infer_from_prompt(text: str, language: Language, accent: Accent, file_location: str) -> Tuple[str, str]:
    result = client.predict(
        text,
        language,
        accent,
        "acou_1",	
        file_location,	
        fn_index=5
    )

    return result

def infer_long_text(text: str, file_location: str, language: Language, accent: Accent) -> Tuple[str, str]:
    result = client.predict(
        text,
        language,
        accent,
        "acou_1",	
        file_location,	
        fn_index=7
    )

    return result
