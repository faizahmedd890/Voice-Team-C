# My Voice Assistant Project Journey

This folder is my next step after Sprint 1 TTS research (`team-c-voice/tts/`).

## One task, three requirements (team lead)

This is one deliverable — an interactive spoken assistant — not two separate projects. I split it into folders for organization (`pipeline/` vs `asr_baseline/`), which can read like two tasks even though it is one.

| # | Requirement | Where it lives | Status |
|---|---|---|---|
| 1 | Voice in → LLM answer (Groq **`llama-3.1-8b-instant`**) | `pipeline/run_voice_demo.py` + `llm_groq.py` | Built, tested |
| 2 | LLM answer → speech out (gTTS preferred) | `pipeline/tts_output.py` | Built, tested |
| 3 | Add noise → Whisper → WER (English ASR baseline, WER < 20%) | `asr_baseline/evaluate_asr_wer.py` | **Done** — PASS at 15 dB SNR |

Abbreviations: ASR = Automatic Speech Recognition, LLM = Large Language Model, TTS = Text-to-Speech, WER = Word Error Rate, SNR = Signal-to-Noise Ratio.

### How requirement 3 connects to the interactive assistant

Both paths use the same ASR engine — **Whisper `small`**:
- **Interactive assistant (`pipeline/transcribe.py`):** mic capture → Whisper → Groq **`llama-3.1-8b-instant`** → gTTS reply.
- **ASR baseline (`asr_baseline/evaluate_asr_wer.py`):** test audio + controlled noise → Whisper → compare to known text → WER score.

The baseline script is not called during a live conversation. It is how I check requirement 3 (WER under noise) before relying on Whisper in the voice demo.

```
Requirement 1+2 (runtime):     mic → Whisper → Groq (llama-3.1-8b-instant) → gTTS
Requirement 3 (validation):  test speech + noise → Whisper → WER vs ground truth
                                      ↑
                              same Whisper model
```

**Mic vs gTTS in requirement 3:** The interactive assistant already uses a real microphone (requirement 1). Requirement 3 is different — it needs **known correct text** to compute WER, plus **controlled noise levels** (15 dB SNR). That is why the baseline uses gTTS-generated speech today: repeatable ground truth. A good next step is to record the same test sentences via mic in `run_voice_demo.py` and re-run WER — that would tie validation closer to real usage.

### Why WER does not run during live conversation

WER (Word Error Rate) needs two things:
1. **Ground-truth text** — the exact sentence that should have been spoken.
2. **Whisper prediction** — what Whisper actually transcribed.

In a live assistant, the user can say anything. I don't have ground truth text in advance, so I can't compute WER on the fly. The mic gives real speech (requirement 1), but WER stays an offline test metric.

That is why requirement 3 is a separate script: fixed test sentences from the CSV, known text, controlled noise, then WER. The voice demo still uses the same Whisper model I tested there.

### WAV vs MP3 — why different formats show up

This is not “ASR uses WAV, assistant uses MP3.” Both flows use both formats at different steps:

| Step | ASR baseline | Interactive pipeline |
|---|---|---|
| Speech source | gTTS → **MP3** | Mic → **WAV** |
| Noisy / raw samples | **WAV** (after noise mixing in numpy) | — |
| Assistant reply | — | gTTS → **MP3** |

Simple rule I follow:
- **WAV** when I have **raw audio samples** — mic capture (`voice_capture.py`), or adding noise in numpy and saving with `scipy.io.wavfile` (`evaluate_asr_wer.py`).
- **MP3** when **gTTS** produces speech — baseline clean source and assistant spoken answers (`tts_output.py`). That is gTTS’s default output.

Whisper accepts both (via ffmpeg). The format choice is about **how the file was created**, not a different ASR engine.

I keep this file as my learning log. Other docs:
- `README.md` — quick index + run commands
- `CHALLENGES.md` — blockers and fixes
- `asr_baseline/README.md` — requirement 3 (WER baseline)
- `pipeline/README.md` — requirements 1+2 (spoken assistant flow)

---

## Why I created a separate folder

Sprint 1 `tts/` was engine comparison work (gTTS vs Coqui).  
This folder is product-style pipeline work, so I kept it separate on purpose.

Sprint 1 challenges: `team-c-voice/tts/CHALLENGES.md`  
This sprint: `CHALLENGES.md` (same folder as this file).

---

## Folder structure

```
team-c-voice/voice_assistant/
├── PROJECT_JOURNEY.md          # main learning log (this file)
├── README.md                   # quick index + run commands
├── CHALLENGES.md               # blockers and fixes for this sprint
├── data/
│   └── load_utterances.py      # loads test sentences from for_reference CSV
├── asr_baseline/               # requirement 3: noisy WER baseline
│   ├── evaluate_asr_wer.py
│   ├── noise_utils.py
│   └── README.md
├── pipeline/                   # requirements 1 + 2: spoken assistant
│   ├── run_voice_demo.py       # mic → Whisper → Groq → gTTS
│   ├── run_text_demo.py        # text → Groq → gTTS (no mic)
│   ├── voice_capture.py        # mic + Silero VAD
│   ├── transcribe.py           # Whisper
│   ├── llm_groq.py             # Groq API
│   ├── tts_output.py           # gTTS reply MP3
│   └── README.md
└── outputs/                    # generated audio + reports (not hand-edited)
    ├── pipeline_capture/       # mic WAV from voice demo
    ├── pipeline_replies/       # gTTS MP3 replies
    ├── asr_baseline_audio/     # baseline test audio by run timestamp
    └── asr_baseline_reports/   # WER CSV reports
```

Output paths are anchored to `voice_assistant/` in code, so files go here even if I run a script from another working directory.

---

## Current tool choices (with reason)

| Layer | Tool | Why |
|---|---|---|
| ASR | Whisper | Team guideline |
| Live capture | Silero Voice Activity Detection (VAD) | Better stop/start for mic input |
| LLM | Groq API — **`llama-3.1-8b-instant`** | Team direction + my preference; set in `llm_groq.py` |
| TTS | gTTS | Lighter and faster in my earlier tests |

Reference reviewed (not edited): `for_reference/c8sud2.py`, `for_reference/streamfinal.py`.

### Default models (if I don't pass flags)

| Step | Default | Where set |
|---|---|---|
| ASR (Whisper) | `small` | `run_voice_demo.py`, `transcribe.py`, `evaluate_asr_wer.py` |
| LLM (Groq) | `llama-3.1-8b-instant` | `llm_groq.py` |
| TTS | gTTS English | `tts_output.py` |

Running `python .../run_voice_demo.py` with **no** `--whisper-model` flag is the same as `--whisper-model small`. There is no other hidden model. To try a different Whisper size: `tiny`, `base`, `small`, `medium`, `large` (trade-off: speed vs accuracy).

---

## What is implemented now

- ASR baseline script: `asr_baseline/evaluate_asr_wer.py` (**full pass-gate run complete** — see below)
- Text pipeline demo: `pipeline/run_text_demo.py`
- Voice pipeline demo: `pipeline/run_voice_demo.py`

Groq key is stored in repo-root `.env` as `GROQ_API_KEY`. LLM model: **`llama-3.1-8b-instant`**.

---

## ASR baseline result (full run, 15 dB SNR)

Official pass-gate run completed on the full filtered set:

| Item | Value |
|---|---|
| Utterances | 60 (`in_scope` + `safe`) |
| Whisper model | `small` |
| Noise condition | 15 dB SNR |
| Mean WER | **0.1418** (14.18%) |
| Team gate (< 20%) | **PASS** |
| Report | `outputs/asr_baseline_reports/asr_wer_results_20260601_174812.csv` |

A few utterances still scored high WER on their own (e.g. place names like Thimphu, acronyms like BHU), but the overall mean clears the gate. Test speech is still gTTS-generated — mic recordings of the same sentences would be a stronger check later.

---

## Test case sources I am using

From reference files (English text, public-service style):

- `for_reference/bhutan classifier test set.csv`
  - I filter `in_scope` + `safe` rows
- `for_reference/IntentMap_UserQuestionCatalogue.xlsx`
  - used as extra phrasing reference

Example test utterances:
- "Where is permit office in Thimphu?"
- "How to check my permit application?"
- "What papers I need register business?"

---

## Noisy WER pass gate — what I changed

My first version checked pass/fail on **clean** audio only. I changed that after re-reading the team requirement: real voice input will have background noise, so the gate should use noisy audio.

Current pass gate:

**WER < 20% on noisy audio at 15 dB SNR.**

If noisy WER passes at 15 dB, clean WER should usually be lower (clean is easier).

### How I arrived at 15 dB (multi-SNR exploration)

I tried a few SNR (Signal-to-Noise Ratio) settings before settling on one gate:

1. **Clean audio only (first version)**  
   Clean WER looked good, but that does not match noisy real-world mic input.

2. **Noisy audio required**  
   Pass/fail must use noisy audio, not clean.

3. **Three SNR levels together (20 / 15 / 10 dB)**  
   I ran exploratory tests so one easy level would not hide bad results at harder noise.  
   Example small run (3 utterances, Whisper `small`, seed 42):  
   - 20 dB mean WER: **0.089**  
   - 15 dB mean WER: **0.275**  
   - 10 dB mean WER: **0.208**  
   Report: `outputs/asr_baseline_reports/asr_wer_results_20260601_174141.csv`

4. **Why I use 15 dB only for the official gate**  
   - **20 dB** — mild noise; felt too easy as the only gate.  
   - **10 dB** — useful stress test, but harsh as the only gate for a first baseline.  
   - **15 dB** — middle ground; one number to report, moderate office-like noise.

I still keep `--explore-snr` so I can re-run 20 / 15 / 10 dB when comparing models or after adding real mic recordings.

What I changed in code:
- Default run evaluates **15 dB SNR only**.
- Clean audio is optional reference only (`--include-clean`).
- `--explore-snr` keeps the earlier 20 / 15 / 10 dB comparison path documented above.

---

## Quick commands

Run from **repo root** (`Voice-Team-C/`). Setup: `pip install -r requirements.txt` and `GROQ_API_KEY` in repo-root `.env`.

ASR baseline pass-gate run (15 dB, 10 utterances):

```bash
python team-c-voice/voice_assistant/asr_baseline/evaluate_asr_wer.py --limit 10 --whisper-model small
```

Full ASR baseline (60 utterances, reported PASS run):

```bash
python team-c-voice/voice_assistant/asr_baseline/evaluate_asr_wer.py --whisper-model small
```

Exploratory 20 / 15 / 10 dB comparison:

```bash
python team-c-voice/voice_assistant/asr_baseline/evaluate_asr_wer.py --limit 10 --explore-snr --whisper-model small
```

With clean reference:

```bash
python team-c-voice/voice_assistant/asr_baseline/evaluate_asr_wer.py --limit 10 --include-clean --whisper-model small
```

Text pipeline:

```bash
python team-c-voice/voice_assistant/pipeline/run_text_demo.py --text "Where is permit office in Thimphu?"
```

Voice pipeline (default Whisper `small`; speak when prompted, pause ~1 s when done):

```bash
python team-c-voice/voice_assistant/pipeline/run_voice_demo.py
```

Windows OpenMP workaround if needed:

```powershell
$env:KMP_DUPLICATE_LIB_OK='TRUE'
python team-c-voice/voice_assistant/pipeline/run_voice_demo.py
```

Shorter index: `README.md` in this folder.

---

## Points to discuss with team

See `CHALLENGES.md` section 7. Main topics: mic-based WER vs gTTS-only baseline, and whether RAG/controller is in scope next.

I will keep updating this file as I learn.
