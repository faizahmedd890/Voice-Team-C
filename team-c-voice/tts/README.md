# TTS Exploration (Sprint 1)

gTTS vs Coqui TTS comparison for English government-style sentences.

- Comparison summary: **`TTS_COMPARISON.md`**
- Blockers: **`CHALLENGES.md`**
- gTTS track: **`gtts/README.md`**
- Coqui track: **`coqui_tts/README.md`**

Run commands below from the **repo root** (`Voice-Team-C/`).

---

## Setup (once)

```bash
pip install -r requirements.txt
```

For Coqui, if needed:

```bash
pip install "coqui-tts[codec]"
pip install "transformers>=4.40,<5.0"
```

For evaluation with proxy WER, ffmpeg (or `pip install imageio-ffmpeg`).

---

## gTTS

Demo:

```bash
python team-c-voice/tts/gtts/run_gtts_demo.py --text "Your registration is completed."
```

Evaluation:

```bash
python team-c-voice/tts/gtts/evaluate_gtts.py --repeats 3 --whisper-model tiny
```

Without ASR (no ffmpeg yet):

```bash
python team-c-voice/tts/gtts/evaluate_gtts.py --repeats 3 --skip-asr
```

---

## Coqui TTS

Demo:

```bash
python team-c-voice/tts/coqui_tts/run_coqui_demo.py --text "Your registration is completed."
```

Evaluation:

```bash
python team-c-voice/tts/coqui_tts/evaluate_coqui.py --repeats 1 --whisper-model tiny
```

Without ASR:

```bash
python team-c-voice/tts/coqui_tts/evaluate_coqui.py --repeats 1 --skip-asr
```
