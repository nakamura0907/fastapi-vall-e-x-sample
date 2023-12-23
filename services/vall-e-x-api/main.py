from fastapi import FastAPI
from pydantic import BaseModel
from gradio_client import Client
from minio import Minio

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

class VoiceModelRequest(BaseModel):
    file_location: str

@app.post("/voice-model/{user_id}")
async def generate_voice_model_handler(user_id: str, body: VoiceModelRequest):
    # 音声モデルの生成

    # ストレージへ保存
    return {"status": "ok"}

class AudioRequest(BaseModel):
    ar_assets_id: str
    text: str
    file_location: str

@app.post("/voice-model/{user_id}/audio")
async def generate_audio_handler(user_id: str, body: AudioRequest):
    # 音声ファイルの生成

    # ストレージへ保存
    return {"status": "ok"}

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

minio_client = Minio(minio_endpoint, access_key=access_key, secret_key=secret_key, secure=False)

def upload_file(file_path: str, bucket_name: str, object_name: str):
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
        minio_client.set_bucket_policy(bucket_name, '', Minio.Policy.READ_ONLY)
    
    minio_client.fput_object(bucket_name, object_name, file_path)