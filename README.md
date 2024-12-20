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

#### Setup html

Enter the same app id above on the UI for APP Id field  
Enter temp token from agora  
Click on configure  
Join the channel by clicking on Join Channel button  
Start specking

output:

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
