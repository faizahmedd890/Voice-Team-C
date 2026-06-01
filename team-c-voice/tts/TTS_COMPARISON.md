# My gTTS vs Coqui TTS Comparison (Sprint 1)

I explored both engines with the same sentence set so I could compare them fairly.

## What I tested

- gTTS folder: `team-c-voice/tts/gtts/`
- Coqui folder: `team-c-voice/tts/coqui_tts/`
- Same 10 government-style sentences in both tracks
- Same evaluation style: latency, success rate, and optional Whisper proxy WER

## Results from my runs

| Metric | gTTS | Coqui TTS |
|---|---:|---:|
| Success rate | 100% | 100% |
| Mean latency | ~0.36 sec | ~1.88 sec |
| P95 latency | ~0.64 sec | ~5.19 sec |
| Mean proxy WER | ~0.047 | ~0.097 |

Source reports I used:
- gTTS: `gtts/outputs/gtts_eval_reports/gtts_eval_results_20260528_224557.csv`
- Coqui: `coqui_tts/outputs/coqui_eval_reports/coqui_eval_results_20260528_225803.csv`

## How to reproduce (run from repo root)

Setup: `pip install -r requirements.txt`

gTTS eval (same style as my comparison run):

```bash
python team-c-voice/tts/gtts/evaluate_gtts.py --repeats 1 --whisper-model tiny
```

Coqui eval:

```bash
python team-c-voice/tts/coqui_tts/evaluate_coqui.py --repeats 1 --whisper-model tiny
```

Quick demos:

```bash
python team-c-voice/tts/gtts/run_gtts_demo.py --text "Your registration is completed."
python team-c-voice/tts/coqui_tts/run_coqui_demo.py --text "Your registration is completed."
```

Full command lists: `README.md` (this folder), `gtts/README.md`, `coqui_tts/README.md`.

## What I learned practically

| Area | gTTS | Coqui TTS |
|---|---|---|
| Setup effort | Easy | Harder (model download, extra dependencies) |
| Internet needed | Yes | No (after model is downloaded) |
| Speed | Faster per sentence | Slower per sentence |
| Output format | MP3 | WAV |
| Voice customization | Limited | More possible (but I used a basic English model first) |
| First-run experience | Quick output | Slow first run (model load/download) |

## My current Sprint 1 view

- **gTTS** is strong for fast MVP delivery and simple team onboarding.
- **Coqui** is strong when offline operation matters, but setup and runtime cost are higher.
- Automated proxy WER helped me check intelligibility, but it is not enough alone for final voice-quality judgment.
- For a final production pick, the team may also want listener scores (`human_eval_template.csv` in both folders) — see **Points to discuss** in `CHALLENGES.md`.

## My tentative MVP direction

For Sprint 1 MVP, I lean toward **gTTS** because of lower latency and easier setup.  
Coqui stays a possible offline backup if internet reliability becomes a blocker in deployment.

## Points to discuss with team

- Language and voice requirements for Bhutan-specific use cases (my runs were English-only).
- How much to weight human listening vs automated metrics when locking the TTS engine.

This comparison is based on my own exploration notes and run outputs, not a production benchmark.
