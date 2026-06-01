# Voice Assistant (Sprint 2)

Spoken assistant: mic/text → Whisper → Groq **`llama-3.1-8b-instant`** → gTTS, plus noisy ASR WER baseline.

Main learning log: **`PROJECT_JOURNEY.md`**  
Blockers: **`CHALLENGES.md`**

Run commands below from the **repo root** (`Voice-Team-C/`).

---

## Setup (once)

```bash
pip install -r requirements.txt
```

Repo-root `.env` (copy from `.env.example`, replace with your key — do not commit `.env`):

```env
GROQ_API_KEY=your_key_here
```

---

## Pipeline (requirements 1 + 2)

Text demo (Groq + gTTS, no mic):

```bash
python team-c-voice/voice_assistant/pipeline/run_text_demo.py --text "Where is permit office in Thimphu?"
```

Voice demo (mic → Whisper → Groq → gTTS). Default Whisper model is **`small`**:

```bash
python team-c-voice/voice_assistant/pipeline/run_voice_demo.py
```

On Windows, if OpenMP error appears:

```powershell
$env:KMP_DUPLICATE_LIB_OK='TRUE'
python team-c-voice/voice_assistant/pipeline/run_voice_demo.py
```

More detail: `pipeline/README.md`

---

## ASR baseline (requirement 3)

Pass gate: mean WER **< 20%** at **15 dB SNR**, Whisper **`small`**.

Quick test (10 utterances):

```bash
python team-c-voice/voice_assistant/asr_baseline/evaluate_asr_wer.py --limit 10 --whisper-model small
```

Full filtered set (60 utterances):

```bash
python team-c-voice/voice_assistant/asr_baseline/evaluate_asr_wer.py --whisper-model small
```

Exploratory 20 / 15 / 10 dB SNR:

```bash
python team-c-voice/voice_assistant/asr_baseline/evaluate_asr_wer.py --limit 10 --explore-snr --whisper-model small
```

More detail: `asr_baseline/README.md`

---

## Outputs

Under `voice_assistant/outputs/`:

- `pipeline_capture/` — mic WAV
- `pipeline_replies/` — gTTS reply MP3
- `asr_baseline_audio/` — baseline test audio
- `asr_baseline_reports/` — WER CSV reports
