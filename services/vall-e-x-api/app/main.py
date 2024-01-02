import os
from dataclasses import dataclass
from fastapi import FastAPI,  File, UploadFile, HTTPException, Depends, Form
from fastapi.responses import JSONResponse
from gradio_client import Client
from minio import Minio
from pydantic import BaseModel
from tempfile import NamedTemporaryFile
from typing import Optional

app = FastAPI()
client = Client("https://plachta-vall-e-x.hf.space/")


#                                                              
#                                                              
#                                                              
# ■■■■■                                                        
# ■    ■                                                       
# ■    ■■  ■■■■  ■■■■   ■■■■   ■   ■■  ■ ■■  ■■■■   ■■■■  ■■■■ 
# ■    ■  ■■  ■  ■     ■■  ■■  ■   ■■  ■■   ■■  ■  ■■  ■  ■    
# ■■■■■   ■   ■■ ■     ■    ■  ■   ■■  ■■   ■      ■   ■■ ■    
# ■   ■   ■■■■■■  ■■   ■    ■  ■   ■■  ■    ■      ■■■■■■  ■■  
# ■    ■  ■         ■  ■    ■  ■   ■■  ■    ■      ■         ■ 
# ■    ■■ ■■     ■  ■  ■■  ■■  ■■  ■■  ■    ■■  ■  ■■     ■  ■ 
# ■     ■  ■■■■  ■■■■   ■■■■    ■■■■■  ■     ■■■■   ■■■■  ■■■■ 
#                                                              
#                                                              

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/voice-model/{user_id}")
def generate_voice_model_handler(user_id: str, file: UploadFile = File(...)):
    temp = NamedTemporaryFile(delete=False)
    try:
        try:
            contents = file.file.read()
            with temp as f:
                f.write(contents)
        except Exception:
            raise HTTPException(
                status_code=500, detail='Error on uploading the file')
        finally:
            file.file.close()

        # 音声モデルの生成
        npz_file_path = make_prompt(user_id, temp.name)

        # ストレージへ保存
        npz_file_name = f"{user_id}.npz"
        upload_file(npz_file_path, "voice-model", npz_file_name)

        return {"status": "ok"}

    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    finally:
        os.remove(temp.name)


class AudioRequest(BaseModel):
    ar_assets_id: str
    text: str


@app.post("/voice-model/{user_id}/audio")
def generate_audio_handler(user_id: str, body: AudioRequest):
    # 音声モデルのダウンロード
    model_name = f"{user_id}.npz"
    download_path = f"/tmp/{user_id}/model.npz"

    download_file("voice-model", model_name, download_path)

    # 音声ファイルの生成
    wav_file_path = infer_from_prompt(body.text, download_path)

    # ストレージへ保存
    audio_name = f"{body.ar_assets_id}.wav"
    upload_file(wav_file_path, "audio", audio_name)

    # 一時保存ファイルの削除
    os.remove(download_path)

    return {"status": "ok"}


@dataclass
class PostPromptRequest:
    trainAudioFile: UploadFile = File(...)
    transcript: Optional[str] = Form(None)


@app.post("/prompts")
def post_prompt(form_data: PostPromptRequest = Depends()):
    content = {"detail": "Function not implemented"}
    return JSONResponse(content=content, status_code=501)

#                                                   
#                                                   
#                  ■   ■                            
#  ■■     ■        ■   ■        ■■■■■■      ■     ■ 
#   ■    ■■        ■   ■        ■           ■■   ■  
#   ■    ■   ■■■   ■   ■        ■            ■■ ■■  
#   ■■   ■  ■   ■  ■   ■        ■             ■■■   
#    ■  ■■      ■  ■   ■        ■■■■■■        ■■    
#    ■  ■   ■■■■■  ■   ■   ■■■  ■             ■■■   
#    ■■ ■   ■   ■  ■   ■        ■            ■■ ■■  
#     ■■    ■  ■■  ■   ■        ■           ■■   ■  
#     ■■    ■■■■■  ■   ■        ■■■■■■      ■     ■ 
#                                                   
#                                                   


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

#                                    
#                                    
#                                    
# ■■     ■■■  ■           ■          
# ■■■    ■■■                         
# ■■■    ■■■  ■   ■ ■■■   ■    ■■■■  
# ■ ■   ■■■■  ■   ■■  ■■  ■   ■■  ■■ 
# ■  ■  ■ ■■  ■   ■    ■  ■   ■    ■ 
# ■  ■  ■ ■■  ■   ■    ■  ■   ■    ■ 
# ■  ■■■  ■■  ■   ■    ■  ■   ■    ■ 
# ■   ■■  ■■  ■   ■    ■  ■   ■■  ■■ 
# ■   ■   ■■  ■   ■    ■  ■    ■■■■  
#                                    
#                                    


minio_endpoint = 'minio:9000'
access_key = 'minio'
secret_key = 'minio123'

minio_client = Minio(minio_endpoint, access_key=access_key,
                     secret_key=secret_key, secure=False)

policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "*"
                ]
            },
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::audio/*"
            ]
        }
    ]
}


def upload_file(file_path: str, bucket_name: str, object_name: str):
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    minio_client.fput_object(bucket_name, object_name, file_path)


def download_file(bucket_name: str, object_name: str, file_path: str):
    minio_client.fget_object(bucket_name, object_name, file_path)
