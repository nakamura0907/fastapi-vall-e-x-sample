import re
from typing import Union, Tuple
from gradio_client import Client


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
        raise ValueError("Prompt result is invalid")
    