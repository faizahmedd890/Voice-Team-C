import threading
import torch
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os
import queue
import time
import csv

whisper_model = whisper.load_model("base")

SAMPLE_RATE = 16000

audio_queue = queue.Queue()
full_audio = []
recording = True

csv_file = "latency_results.csv"

if not os.path.exists(csv_file):
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Recording Duration",
            "Whisper Processing Time",
            "Total Pipeline Time"
        ])

def audio_callback(indata, frames, time_info, status):
    global recording

    if recording:
        audio_queue.put(indata.copy())

def stop_recording():
    global recording

    input("Press Enter to stop recording...\n")

    recording = False

print("Speak now...")
print("Recording started")

total_start = time.time()
recording_start = time.time()

threading.Thread(target=stop_recording, daemon=True).start()

with sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype='float32',
    callback=audio_callback
):

    while True:

        if not recording and audio_queue.empty():
            break

        try:
            chunk = audio_queue.get(timeout=0.1)

            chunk = chunk.flatten()

            full_audio.extend(chunk)

        except queue.Empty:
            continue

recording_end = time.time()

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

whisper_start = time.time()

result = whisper_model.transcribe(temp_wav.name)

whisper_end = time.time()

total_end = time.time()

recording_duration = recording_end - recording_start
whisper_duration = whisper_end - whisper_start
total_duration = total_end - total_start

print("\nTranscription:")
print(result["text"])

print("\n===== LATENCY RESULTS =====")
print(f"Recording Duration: {recording_duration:.2f} sec")
print(f"Whisper Processing Time: {whisper_duration:.2f} sec")
print(f"Total Pipeline Time: {total_duration:.2f} sec")

with open(csv_file, mode="a", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        round(recording_duration, 2),
        round(whisper_duration, 2),
        round(total_duration, 2)
    ])

os.remove(temp_wav.name)