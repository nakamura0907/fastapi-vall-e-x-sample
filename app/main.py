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
    result3 = client.predict(
                    "user-id",	# str in 'Prompt name' Textbox component
                    url,	# str (filepath or URL to file) in 'uploaded audio prompt' Audio component
                    url,	# str (filepath or URL to file) in 'recorded audio prompt' Audio component
                    "",	# str in 'Transcript' Textbox component
                    fn_index=3
    )
    print(result3)
    _, file_path3 = result3

    result5 = client.predict(
                    "こんにちは、人間です",	# str in 'Text' Textbox component
                    "日本語",	# str (Option from: ['auto-detect', 'English', '中文', '日本語', 'Mix']) in 'language' Dropdown component
                    "日本語",	# str (Option from: ['no-accent', 'English', '中文', '日本語']) in 'accent' Dropdown component
                    "acou_1",	# str (Option from: ['acou_1', 'acou_2', 'acou_3', 'acou_4', 'alan', 'amused', 'anger', 'babara', 'bronya_1', 'cafe', 'dingzhen', 'dingzhen_1', 'disgust', 'emo_amused', 'emo_anger', 'emo_neutral', 'emo_sleepy', 'emotion_sleepiness', 'en2zh_tts_1', 'en2zh_tts_2', 'en2zh_tts_3', 'en2zh_tts_4', 'esta', 'fuxuan_2', 'librispeech_1', 'librispeech_2', 'librispeech_3', 'librispeech_4', 'neutral', 'paimon_1', 'prompt_1', 'rosalia', 'seel', 'seel_1', 'sleepiness', 'vctk_1', 'vctk_2', 'vctk_3', 'vctk_4', 'yaesakura', 'yaesakura_1', 'zh2en_tts_1', 'zh2en_tts_2', 'zh2en_tts_3', 'zh2en_tts_4']) in 'Voice preset' Dropdown component
                    file_path3,	# str (filepath or URL to file) in 'parameter_46' File component
                    fn_index=5
    )

    print(result5)
    _, audio_path5 = result5

    return {"Hello": "World"}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def time_consuming_task():
    logger.info("A関数を開始します")
    time.sleep(5)
    logger.info("A関数が完了しました")

@app.post("/voice-model/{user_id}")
async def generate_voice_model(user_id: str, body: dict, background_tasks: BackgroundTasks):
    file = body.get("file")
    if not file:
        return HTTPException(status_code=400, detail="File is required")
    
    print(file)
    print(user_id)

    background_tasks.add_task(time_consuming_task)

    return {"Hello": "World"}

@app.post("/voice-model/{user_id}/sound")
async def generate_voice_model_sound(user_id: str, body: dict, background_tasks: BackgroundTasks):
    text = body.get("text")
    if not text:
        return HTTPException(status_code=400, detail="text is required")
    
    print(text)
    print(user_id)

    background_tasks.add_task(time_consuming_task)

    return {"Hello": "World"}