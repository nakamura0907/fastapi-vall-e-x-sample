from typing import Literal


Language = Literal["auto-detect", "English", "中文", "日本語"]
Accent = Literal['no-accent', 'English', '中文', '日本語']
VoicePreset = Literal['acou_1', 'acou_2', 'acou_3', 'acou_4', 'alan', 'amused', 'anger', 'babara', 'bronya_1', 'cafe', 'dingzhen', 'dingzhen_1', 'disgust', 'emo_amused', 'emo_anger', 'emo_neutral', 'emo_sleepy', 'emotion_sleepiness', 'en2zh_tts_1', 'en2zh_tts_2', 'en2zh_tts_3', 'en2zh_tts_4', 'esta', 'fuxuan_2', 'librispeech_1', 'librispeech_2', 'librispeech_3', 'librispeech_4', 'neutral', 'paimon_1', 'prompt_1', 'rosalia', 'seel', 'seel_1', 'sleepiness', 'vctk_1', 'vctk_2', 'vctk_3', 'vctk_4', 'yaesakura', 'yaesakura_1', 'zh2en_tts_1', 'zh2en_tts_2', 'zh2en_tts_3', 'zh2en_tts_4']