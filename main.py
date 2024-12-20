import asyncio
import os
import signal
from multiprocessing import Process
from transformers import pipeline
from agora_realtime_ai_api.rtc import Channel, ChatMessage, RtcEngine, RtcOptions
import torch
import numpy as np
from scipy.io import wavfile
import io
import torchaudio
import logging
import wave
import time
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
model_name = "openai/whisper-tiny"
transcriber = pipeline("automatic-speech-recognition", model=model_name, device=0 if torch.cuda.is_available() else -1)
CHANNEL_NAME = "example_channel"
USERID = 1234
subscribe_user = None

load_dotenv()
def handle_agent_proc_signal(signum, frame):
    os._exit(0)

# Function to run the agent in a new process
async def wait_for_remote_user(channel: Channel) -> int:
    remote_users = list(channel.remote_users.keys())
    if len(remote_users) > 0:
        return remote_users[0]

    future = asyncio.Future[int]()

    channel.once("user_joined", lambda conn, user_id: future.set_result(user_id))

    try:
        # Wait for the remote user with a timeout of 30 seconds
        remote_user = await asyncio.wait_for(future, timeout=15.0)
        return remote_user
    except KeyboardInterrupt:
        future.cancel()
        
    except Exception as e:
        print(f"Error waiting for remote user: {e}")
        raise

def run_agent_in_process(engine_app_id: str, engine_app_cert: str, channel_name: str, uid: int):
    signal.signal(signal.SIGINT, handle_agent_proc_signal)  # Forward SIGINT
    signal.signal(signal.SIGTERM, handle_agent_proc_signal)  # Forward SIGTERM
    asyncio.run(
        setup_and_run_agent(
            engine=RtcEngine(appid=engine_app_id, appcert=engine_app_cert),
            options=RtcOptions(
                channel_name=channel_name,
                uid=uid,
                sample_rate=16000,  # PCM_SAMPLE_RATE
                channels=1,  # PCM_CHANNELS
                enable_pcm_dump=os.environ.get(
                    "WRITE_RTC_PCM", "false") == "true"
            )
        )
    )

# Function to set up and run the agent
async def setup_and_run_agent(engine: RtcEngine, options: RtcOptions):
    channel = engine.create_channel(options)
    await channel.connect()

    subscribe_user = await wait_for_remote_user(channel)
    print(f"Subscribing to user {subscribe_user}")
    await channel.subscribe_audio(subscribe_user)
    async for frames in collect_audio_frames(channel, subscribe_user, interval=4):
        print(f"Collected {len(frames)} frames over 4 seconds.")
        audio_data = b''.join(frames)    
        audio_np = np.frombuffer(audio_data, dtype=np.int16)

        # Ensure the numpy array is single-channel (reshape if necessary)
        if audio_np.ndim > 1:
            audio_np = audio_np[:, 0]

        # Normalize the waveform
        waveform_np = audio_np.astype(np.float32) / (2**15)

        # Process the waveform using the Whisper model
        transcription = transcriber(waveform_np)
        print("Transcription: %s", transcription['text'])
    

async def collect_audio_frames(channel, subscribe_user, interval=4):
    """
    Collects audio frames for a specified interval (e.g., 4 seconds) and yields them.

    :param channel: The channel object providing audio frames.
    :param subscribe_user: The user to subscribe to for audio frames.
    :param interval: The duration to collect audio frames (in seconds).
    """
    while True:
        frames = []
        start_time = asyncio.get_event_loop().time()
        async for audio_frame in channel.get_audio_frames(subscribe_user):
            frames.append(audio_frame.data)

            # Break after the interval
            if asyncio.get_event_loop().time() - start_time >= interval:
                break

        yield frames

# Example usage of running the agent
if __name__ == "__main__":
    app_id = DB_NAME = os.getenv("AGORA_APP_ID") 
    app_cert = os.getenv("AGORA_APP_CERT")
    run_agent_in_process(app_id, app_cert,CHANNEL_NAME, USERID)
