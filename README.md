# Realtime speech recognition

### Realtime speech recognition uses hugging face "openai/whisper-tiny" and "automatic-speech-recognition" transformers to listen to agora realtime audio stream every 4 sec using "agora_realtime_ai_api" to convert speech into text.

#### Setup python

##### 1. Create `.env` file

```bash
cp ./.env.example ./.env
```

#### 2. Setup Agora App ID and App Certificate in `.env`

```bash
AGORA_APP_ID=
AGORA_APP_CERT=
```

#### 3. Run

```bash
python main.py
```

#### Setup html

1. Enter the same app id above on the UI for APP Id field
2. Enter temp token from agora
3. Click on configure
4. Join the channel by clicking on Join Channel button
5. Start specking

Output:

```bash
Transcription: %s  Hi there.
Collected 459 frames over 4 seconds.
Transcription: %s  ah
Collected 423 frames over 4 seconds.
Transcription: %s  is not recognizing.
Collected 427 frames over 4 seconds.
Transcription: %s  will be.
Collected 425 frames over 4 seconds.
Transcription: %s  Thank you.
Collected 422 frames over 4 seconds.
```
