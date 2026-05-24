import torch
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os
import queue
import time

from silero_vad import load_silero_vad
from silero_vad import get_speech_timestamps

vad_model = load_silero_vad()
whisper_model = whisper.load_model("base")

SAMPLE_RATE = 16000
CHUNK_DURATION = 0.5  
SILENCE_LIMIT = 5     

audio_queue = queue.Queue()

full_audio = []

def audio_callback(indata, frames, time_info, status):
    audio_queue.put(indata.copy())

print("Speak now...")

silence_start = None
speech_detected = False

with sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype='float32',
    blocksize=int(SAMPLE_RATE * CHUNK_DURATION),
    callback=audio_callback
):

    while True:

        chunk = audio_queue.get()
        chunk = chunk.flatten()

        full_audio.extend(chunk)
        audio_tensor = torch.from_numpy(chunk)

        speech_timestamps = get_speech_timestamps(
            audio_tensor,
            vad_model,
            sampling_rate=SAMPLE_RATE
        )
        if len(speech_timestamps) > 0:

            if not speech_detected:
                print("Speech detected!")

            speech_detected = True
            silence_start = None

        else:
            if speech_detected:

                if silence_start is None:
                    silence_start = time.time()

                elapsed_silence = time.time() - silence_start

                print(f"Silent for {elapsed_silence:.1f}s", end="\r")

                if elapsed_silence >= SILENCE_LIMIT:
                    print("\nStopping recording...")
                    break

full_audio = np.array(full_audio, dtype=np.float32)

temp_wav = tempfile.NamedTemporaryFile(
    suffix=".wav",
    delete=False
)
temp_wav.close()

wav.write(
    temp_wav.name,
    SAMPLE_RATE,
    (full_audio * 32767).astype(np.int16)
)

result = whisper_model.transcribe(temp_wav.name)

print("\nTranscription:")
print(result["text"])

os.remove(temp_wav.name)