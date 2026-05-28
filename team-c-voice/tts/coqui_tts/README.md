# My Coqui TTS Sprint 1 Notes

I am continuing my TTS exploration with Coqui after gTTS.  
This folder is my offline neural TTS track for Sprint 1 comparison.

## Why I am testing Coqui TTS

- It can run offline after model download.
- Voice quality is usually more natural than basic cloud TTS.
- It is heavier to set up, so I want to measure if that trade-off is worth it for MVP.

## What I built

- `coqui_engine.py`: reusable function to generate WAV and capture latency/errors.
- `run_coqui_demo.py`: single sentence demo runner.
- `evaluate_coqui.py`: benchmark runner for latency, success rate, and optional proxy WER.
- `sample_prompts.py`: fixed sentence list (same style as gTTS for fair comparison).
- `human_eval_template.csv`: manual listening sheet for reviewers.

## Setup notes I learned (important)

1. Install project dependencies:
   - `pip install -r requirements.txt`
2. Coqui on newer PyTorch may need codec support:
   - `pip install "coqui-tts[codec]"`
3. If import fails with transformers error, I use:
   - `pip install "transformers>=4.40,<5.0"`
4. For ASR scoring in evaluation, ffmpeg is still needed (same as gTTS flow):
   - `winget install --id Gyan.FFmpeg --exact`
   - or fallback: `pip install imageio-ffmpeg`

## Default model I started with

- `tts_models/en/ljspeech/tacotron2-DDC`
- Reason: simple English baseline for first sprint comparison.

## How I run it

1. Quick demo:
   - `python team-c-voice/tts/coqui_tts/run_coqui_demo.py --text "Your registration is completed."`
2. Evaluation:
   - `python team-c-voice/tts/coqui_tts/evaluate_coqui.py --repeats 1 --whisper-model tiny`
3. If ffmpeg is not ready yet:
   - `python team-c-voice/tts/coqui_tts/evaluate_coqui.py --repeats 1 --skip-asr`

## First-run behavior (normal)

- First Coqui run downloads model files, so it feels slow.
- `evaluate_coqui.py` loads the model once before sentence loop.
- Per-sentence latency after warm-up is what I compare against gTTS.

## Why repeats matter

`--repeats` means I run the same sentence set multiple times.

- `repeats=1`: quick smoke test
- `repeats=3`: better sprint-level confidence
- `repeats>3`: stronger statistics if needed

## Whisper warning during evaluation (normal on CPU)

When ASR is enabled, I may see:

`FP16 is not supported on CPU; using FP32 instead`

This is expected on CPU and not a failure by itself.

## Quick sanity checklist (before demo)

1. Demo: `python team-c-voice/tts/coqui_tts/run_coqui_demo.py --text "Your registration is completed."`
2. Eval: `python team-c-voice/tts/coqui_tts/evaluate_coqui.py --repeats 1 --whisper-model tiny`
3. Confirm report under `team-c-voice/tts/coqui_tts/outputs/coqui_eval_reports/`

## What I am comparing against gTTS

- Voice quality (human listening + optional proxy WER)
- Latency (mean and P95)
- Offline support (Coqui yes, gTTS no)
- Setup effort (Coqui heavier, gTTS lighter)

My goal here is not to claim winner yet — it is to collect evidence for MVP decision.
