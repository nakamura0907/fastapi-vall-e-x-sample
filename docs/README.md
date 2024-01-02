# システム要件

---

- 音声ファイルをもとにオーディオプロンプトを生成することができる
- オーディオプロンプトとテキストから音声を合成することができる

# ビジネスルール

---

- 音声ファイルは3秒以上、30秒未満である必要がある
- テキストは255文字以下とする

# ユースケース

---

- オーディオプロンプトCUD
    - オーディオプロンプトの生成
    - オーディオプロンプトのPATCH（音声ファイルやTranscriptの変更）
    - オーディオプロンプトの削除
- 合成音声CRUD
    - 合成音声の生成
    - 合成音声の一覧取得
    - 合成音声の取得
    - 合成音声のPATCH
    - 合成音声の削除

# データ設計

---

## ドメイン

**オーディオプロンプト（AudioPrompt）**

- ID
- TrainAudioFile
- Transcript: option

**合成音声（SyntheticVoice）**

- ID
- AudioPromptID
- Text
- Language: option, default “auto-detect”
- Accent: option, default “no-accent”

## データベース設計

**audio_prompts**

- id
- prompt_file_relative_path
- transcript

**synthetic_voices**

- id
- audio_prompt_id
- text
- language
- accent

## ストレージ設計

**train_audios**

**audio_prompts**

**synthetic_voices**