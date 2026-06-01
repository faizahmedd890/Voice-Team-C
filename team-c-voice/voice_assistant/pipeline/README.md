# My Pipeline Notes

This folder is **requirement 1 + 2** of the spoken assistant (see `../PROJECT_JOURNEY.md` for the full picture):

**voice in → Whisper ASR → Groq LLM (`llama-3.1-8b-instant`) → gTTS output**

Requirement 3 (noisy WER baseline) lives in `../asr_baseline/` — it validates the **same Whisper model** this pipeline uses at runtime, but WER scoring only runs in that test script, not during live conversation.

Abbreviations:
- ASR = Automatic Speech Recognition
- LLM = Large Language Model
- TTS = Text-to-Speech
- VAD = Voice Activity Detection

---

## Scripts

- `run_text_demo.py` — text question → Groq answer → gTTS MP3
- `run_voice_demo.py` — mic (Silero VAD) → Whisper → Groq → gTTS MP3

---

## Test cases I use for quick checks

Text demo:
- "Where is permit office in Thimphu?"
- "How to check my permit application?"
- "What papers I need register business?"

Voice demo:
- I speak one of the same style questions into mic and check:
  1. transcription text
  2. Groq answer text
  3. generated MP3 reply path

These are smoke tests, not full WER evaluation.

---

## Groq setup

Model: **`llama-3.1-8b-instant`** (set in `llm_groq.py`).

Repo-root `.env` (copy from repo-root `.env.example`, add your key):

```env
GROQ_API_KEY=your_key_here
```

I keep my real key in `.env` locally (not committed).

---

## Setup

From **repo root** (`Voice-Team-C/`):

```bash
pip install -r requirements.txt
```

---

## Run commands

Text demo:

```bash
python team-c-voice/voice_assistant/pipeline/run_text_demo.py --text "Where is permit office in Thimphu?"
```

Voice demo (default Whisper model is **`small`** — same as passing `--whisper-model small`):

```bash
python team-c-voice/voice_assistant/pipeline/run_voice_demo.py
```

Speak as soon as you see the prompt; pause ~1 second when finished (VAD detects end of speech).

Optional explicit Whisper model flag:

```bash
python team-c-voice/voice_assistant/pipeline/run_voice_demo.py --whisper-model small
```

---

## Outputs

All paths are under `voice_assistant/outputs/` (fixed in code — same location whether you run from repo root or `pipeline/`).

- Captured user audio: `voice_assistant/outputs/pipeline_capture/`
- Assistant reply audio: `voice_assistant/outputs/pipeline_replies/`

---

## Notes from my first setup

- Silero VAD is used only in voice demo capture.
- WER baseline (requirement 3) is in `../asr_baseline/` — same Whisper engine, separate validation script.
- Blockers log: `../CHALLENGES.md`

If you see `OMP: Error #15: Initializing libiomp5md.dll...`, that is PyTorch + NumPy both loading OpenMP on Windows. `run_voice_demo.py` sets `KMP_DUPLICATE_LIB_OK=TRUE` at startup. You can also run:

```powershell
$env:KMP_DUPLICATE_LIB_OK='TRUE'
python team-c-voice/voice_assistant/pipeline/run_voice_demo.py
```
