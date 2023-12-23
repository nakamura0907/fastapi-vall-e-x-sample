# main.py
import logging
import time
from fastapi import FastAPI, BackgroundTasks, HTTPException
from gradio_client import Client

app = FastAPI()

client = Client("https://plachta-vall-e-x.hf.space/")
url = "https://plachta-vall-e-x.hf.space/file=/tmp/gradio/5e9ca449d130b545d2c6d4600d196a4e778f5261/ja-2.ogg"

@app.get("/")
def read_root():
    return {"Hello": "World"}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def time_consuming_task():
    logger.info("A関数を開始します")
    time.sleep(5)
    logger.info("A関数が完了しました")

@app.post("/voice-model/{user_id}")
async def generate_voice_model_handler(user_id: str, body: dict, background_tasks: BackgroundTasks):
    file = body.get("file")
    if not file:
        return HTTPException(status_code=400, detail="File is required")
    
    print(file)
    print(user_id)

    background_tasks.add_task(time_consuming_task)

    return {"Hello": "World"}

@app.post("/voice-model/{user_id}/sound")
async def generate_audio_handler(user_id: str, body: dict, background_tasks: BackgroundTasks):
    id = body.get("id")
    text = body.get("text")
    file = body.get("file")

    if not id:
        return HTTPException(status_code=400, detail="id is required")
    if not text:
        return HTTPException(status_code=400, detail="text is required")
    if not file:
        return HTTPException(status_code=400, detail="file is required")
    
    print(text)
    print(user_id)

    background_tasks.add_task(time_consuming_task)

    return {"Hello": "World"}

def generate_voice_model_task(user_id: str, file_location: str):
    # predict
    # save to azure
    # remove from tmp
    return

def generate_audio_task(id: str, file_location: str, text: str):
    # predict
    # save to azure
    # remove from tmp
    return

def make_prompt(prompt_name: str, file_location: str) -> str:
    transcript = ""

    result = client.predict(
        prompt_name,
        file_location,	
        file_location,
        transcript,
        fn_index=3
    )

    _, file_path = result
    return file_path

def infer_from_prompt(text: str, file_location: str) -> str:
    result = client.predict(
        text,
        "日本語",	
        "日本語",	
        "acou_1",	
        file_location,	
        fn_index=5
    )

    _, file_path = result
    return file_path