# main.py
import logging
import os
import time
from azure.storage.blob import BlobServiceClient, ContentSettings
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
    
    background_tasks.add_task(generate_voice_model_task, user_id, file)

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
    
    background_tasks.add_task(generate_audio_task, id, file, text)

    return {"Hello": "World"}

def generate_voice_model_task(user_id: str, file_location: str):
    prompt_path = make_prompt(user_id, file_location)

    # save to storage
    blob_name = f"{user_id}.npz"
    upload_to_storage("test", blob_name, prompt_path)

    # remove from tmp
    # notify backend


    logger.info(f"prompt_path: {prompt_path}")
    logger.info(f"blob_name: {blob_name}")

    return

def generate_audio_task(id: str, file_location: str, text: str):
    blob_service_client = get_azure_client()
    blob_client = blob_service_client.get_blob_client(container="test", blob="1.npz")

    # FIXME: 一旦ダウンロードしないとエラーになる
    download_path = "/tmp/npz/test.npz"
    os.makedirs(os.path.dirname(download_path), exist_ok=True)
    with open(download_path, "wb") as download_file:
        logger.info(f"downloaded blob")
        download_blob = blob_client.download_blob()
        download_file.write(download_blob.readall())
        logger.info(f"downloaded blob")

    audio_path = infer_from_prompt(text, "/tmp/npz/test.npz")

    # save to storage
    blob_name = f"{id}.wav"
    upload_to_storage("test", blob_name, audio_path)

    # remove from tmp
    # notify backend

    logger.info(f"audio_path: {audio_path}")
    logger.info(f"blob_name: {blob_name}")

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

def upload_to_storage(container_name: str, blob_name: str, file_path: str):
    blob_service_client = get_azure_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, content_settings=ContentSettings(content_type="application/octet-stream"))

def get_azure_client():
    connection_string = ""
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    return blob_service_client