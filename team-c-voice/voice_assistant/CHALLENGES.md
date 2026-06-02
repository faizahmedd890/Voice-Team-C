# My Voice Assistant Challenges Log (Sprint 1)

This file tracks the main technical challenges I hit while building the spoken assistant (`voice_assistant/`) in Sprint 1.

Stack for reference: Whisper `small` (ASR) → Groq **`llama-3.1-8b-instant`** (LLM) → gTTS (TTS).

---

## 1) Pass gate on clean audio (first version)

My first ASR baseline checked WER on clean audio only. That was too optimistic for real mic use. I switched the pass gate to noisy audio at **15 dB SNR** after trying 20 / 15 / 10 dB together. Details are in `PROJECT_JOURNEY.md`.

---

## 2) OpenMP error on Windows (`libiomp5md.dll`)

Running `run_voice_demo.py` crashed with `OMP: Error #15` because PyTorch (Silero VAD) and NumPy/SciPy both load OpenMP. I set `KMP_DUPLICATE_LIB_OK=TRUE` at the top of `run_voice_demo.py` (same workaround as the ASR baseline scripts).

---

## 3) Silero VAD — "Input audio chunk is too short"

Silero needs at least **512 samples** at 16 kHz (32 ms). My first chunk size was 30 ms (480 samples), which failed immediately. I changed `voice_capture.py` to use 512-sample chunks.

---

## 4) Output files landing in the wrong folder

Output paths were written as strings like `team-c-voice/voice_assistant/outputs/...` relative to the **current working directory**. Running from inside `pipeline/` created a nested `pipeline/team-c-voice/...` tree. I fixed the demo scripts to use `VA_ROOT / "outputs" / ...` so paths always point to `voice_assistant/outputs/`.

---

## 5) ASR baseline uses gTTS speech, not my mic

For WER I need known ground-truth text and controlled noise (15 dB SNR). I used gTTS-generated speech for repeatability. That passed the team gate (14.18% mean WER on 60 utterances), but it is not the same as human mic audio. Re-recording the same CSV sentences through `run_voice_demo.py` would be a stronger check later.

---

## 6) Groq answers without RAG

The pipeline calls Groq with a short system prompt only — no document retrieval like in `for_reference/c8sud2.py`. Answers can be generic or wrong on specific Bhutan office details. Fine for a first demo; RAG/controller integration would be a later step if the product needs it.

---

## 7) Points to discuss with team

- Re-run WER on mic recordings of the test CSV sentences vs keeping gTTS-only baseline for now.
- Whether RAG / intent controller from reference code is in scope for a follow-up sprint.

---

## Run commands

See `README.md` (quick index), `PROJECT_JOURNEY.md` (full notes), `pipeline/README.md`, and `asr_baseline/README.md`.
