# My TTS Challenges Log (Sprint 1)

This file tracks the main technical challenges I faced while exploring gTTS and Coqui TTS for Sprint 1.

Engines compared: **gTTS** vs **Coqui** (`tts_models/en/ljspeech/tacotron2-DDC` in my runs).

---

## 1) Learning TTS from scratch

I had no prior TTS experience. I started with a simple text-to-speech demo, then added basic evaluation (latency, success rate, and optional proxy WER). Once both engines produced audio, comparison got easier.

---

## 2) ffmpeg setup for evaluation

Whisper-based proxy WER in my evaluation scripts needed ffmpeg to read generated audio. On Windows, PATH setup took extra effort. I used system ffmpeg where possible and a Python fallback (`imageio-ffmpeg`) so evaluation could run on my machine.

Basic TTS demo scripts do not need ffmpeg.

---

## 3) Coqui dependency and setup overhead

Coqui needed more setup than gTTS (dependency/version alignment and `coqui-tts[codec]`). First run also downloaded the model, which slowed initial testing.

After setup, Coqui worked, but effort and runtime were higher than gTTS in my Sprint 1 runs.

---

## 4) Proxy WER vs voice quality

Proxy WER (Whisper transcribing TTS output) helped check basic intelligibility, but it does not capture naturalness or pronunciation quality on its own. Each engine folder has a `human_eval_template.csv` if the team wants listener-based scoring later.

---

## 5) gTTS preference for MVP (cloud context)

Target deploy is likely AWS/cloud, where online services are normal. gTTS needs internet, which fits that context. From my Sprint 1 runs, gTTS was lighter to set up and faster than Coqui, so that is my current preference for MVP — details in `TTS_COMPARISON.md`.

---

## 6) Points to discuss with team

- Language and voice requirements for Bhutan-specific use cases (English-only for now in my work).
- How much to weight human listening scores vs automated metrics when locking the TTS engine for production.

---

## Run commands

See `README.md` in this folder, or engine READMEs: `gtts/README.md`, `coqui_tts/README.md`.
