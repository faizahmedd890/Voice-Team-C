# My gTTS Sprint 1 Notes

I am new to TTS, so this folder is my practical exploration of `gTTS` in a simple and measurable way.

## Why I started with gTTS

- I wanted to start with a tool that is quick to set up.
- I wanted to hear working voice output early in Sprint 1.
- I know it depends on internet, so I am measuring reliability and latency clearly.

## What I built

- `gtts_engine.py`: reusable function to generate MP3 and capture latency/errors.
- `run_gtts_demo.py`: single sentence demo runner.
- `evaluate_gtts.py`: benchmark runner for latency, success rate, and optional proxy WER.
- `sample_prompts.py`: fixed sentence list for fair testing.
- `human_eval_template.csv`: listening test sheet.

## How I run it

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Check if ffmpeg is already installed:
   - `where.exe ffmpeg`
3. If ffmpeg is missing (I hit this once), install it:
   - `winget install --id Gyan.FFmpeg --exact`
4. Restart terminal and verify:
   - `ffmpeg -version`
5. If PATH still does not detect ffmpeg, install Python fallback:
   - `pip install imageio-ffmpeg`
2. Quick demo:
   - `python team-c-voice/tts/gtts/run_gtts_demo.py --text "Your registration is completed."`
3. Evaluation (latency + reliability + optional ASR proxy):
   - `python team-c-voice/tts/gtts/evaluate_gtts.py --repeats 3`
4. If ffmpeg is still not configured correctly:
   - `python team-c-voice/tts/gtts/evaluate_gtts.py --repeats 3 --skip-asr`

## What I learned while setting up ffmpeg

- Whisper-based proxy WER needs ffmpeg to read audio.
- Without ffmpeg, latency and reliability still run, but WER stays empty.
- So I first run with `--skip-asr`, then rerun full evaluation after ffmpeg setup.
- I also added a fallback in `evaluate_gtts.py` that tries Python-managed ffmpeg (`imageio-ffmpeg`) if system PATH fails.

## Why I did not use `ffmpeg-python`

- `ffmpeg-python` is mainly a wrapper to build ffmpeg commands from Python.
- My script uses Whisper directly, and Whisper needs the real ffmpeg executable (`ffmpeg.exe`).
- So I used binary-first setup (`winget` install) plus Python binary fallback (`imageio-ffmpeg`) for reliability.
- I avoided `pip install ffmpeg` because it is a different old package and not what Whisper needs.

## Why repeats matter

`--repeats` means I run the same sentence set multiple times.

- `repeats=1`: quick smoke test (fast, less reliable conclusion)
- `repeats=3`: better confidence for sprint-level decision
- `repeats>3`: stronger statistics if I need more confidence

I use repeats because one run can look good or bad by chance (temporary network fluctuation). Repeats give a more stable average.

## What I check before deciding

- Latency: mean and P95
- Reliability: success percentage
- Intelligibility proxy: Whisper WER (only when ASR is enabled)
- Human listening: naturalness, clarity, pronunciation scores

## Whisper warning during evaluation (normal on CPU)

When I run `evaluate_gtts.py` with ASR enabled, I sometimes see:

`FP16 is not supported on CPU; using FP32 instead`

This is expected on my machine because Whisper tries half-precision first, then falls back to FP32 on CPU. It is not an error and does not mean the run failed. I still check the summary at the end (success rate, latency, proxy WER).

## Quick sanity checklist (before demo)

1. Demo: `python team-c-voice/tts/gtts/run_gtts_demo.py --text "Your registration is completed."`
2. Full eval: `python team-c-voice/tts/gtts/evaluate_gtts.py --repeats 1 --whisper-model tiny`
3. Confirm report exists under `team-c-voice/tts/gtts/outputs/gtts_eval_reports/`

## Current gTTS understanding

- Works fast for MVP
- Very easy setup for the team
- No true offline support
- Voice customization is limited compared to heavier offline TTS models

So for Sprint 1, my goal is to confirm whether this trade-off is acceptable for MVP scope.
