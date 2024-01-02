import re
import os
from dataclasses import dataclass
from fastapi import FastAPI,  File, UploadFile, Depends, Form, status, Response
from gradio_client import Client
from typing import Optional, Union, Tuple
from tempfile import NamedTemporaryFile

app = FastAPI()
client = Client("https://plachta-vall-e-x.hf.space/")


@dataclass
class PostPromptRequest:
    trainAudioFile: UploadFile = File(...)
    transcript: Optional[str] = Form(None)


@app.post(
    "/prompts",
    tags=["prompts"],
    status_code=status.HTTP_201_CREATED,
    response_description="Prompt created",
    response_model=None,
)
async def post_prompt(form_data: PostPromptRequest = Depends()):
    with NamedTemporaryFile(delete=True) as tmp:
        try:
            # Validation

            # Save audio file to temporary file
            # Synthesis audio file only accepts file path or URL as argument
            try:
                contents = form_data.trainAudioFile.file.read()
                with open(tmp.name, "wb") as f:
                    f.write(contents)
            except Exception as e:
                print(e)
                return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal server error")
            finally:
                form_data.trainAudioFile.file.close()

            # Make prompt
            detected_text, prompt_file_path = make_prompt("plachta-vall-e-x", tmp.name, form_data.transcript)

            # Upload train audio file to storage
                
            # Upload prompt file to storage
                
            # Save prompt to database

            # Remove temporary prompt file
            if os.path.exists(prompt_file_path):
                os.remove(prompt_file_path)

            return Response(status_code=status.HTTP_201_CREATED, headers={
                "Location": "/{prompt_id}",
            })
        except Exception as e:
            print(e)
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal server error")

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
    