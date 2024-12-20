# realtime-speech-recognition

## Realtime speech recognition uses hugging face "openai/whisper-tiny" and "automatic-speech-recognition" transformers to listen to agora realtime audio stream every 4 sec using "agora_realtime_ai_api" to convert speech into text.

### setup python

#### 1. Create `.env` file

```bash
cp ./.env.example ./.env
```

#### 2. Setup Agora App ID and App Certificate in `.env`

```bash
AGORA_APP_ID=
AGORA_APP_CERT=
```

### setup html

Enter the same app id above on the UI for APP Id field
Enter temp token from agora
