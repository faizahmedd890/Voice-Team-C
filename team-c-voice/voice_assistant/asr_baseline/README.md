# My ASR Baseline Notes

This folder checks English ASR quality using Whisper and WER (Word Error Rate).

---

## What WER means here

WER = percentage of word mistakes between:
- ground-truth sentence
- Whisper transcription

Team target: **WER < 20%** (same as `< 0.20` in CSV output).

---

## Pass gate (important)

Pass/fail is checked on **noisy audio**, not clean audio.

Reason: in real voice use, some background noise is expected.  
If we pass on noisy audio, clean audio should usually pass automatically.

Default pass condition in my script:
- noisy audio at **15 dB SNR** (Signal-to-Noise Ratio)
- pass if mean WER at 15 dB is **< 20%**

I previously tested **20 / 15 / 10 dB** together. See `../PROJECT_JOURNEY.md` for why I settled on **15 dB only** for the official pass gate. You can still re-run the multi-level comparison with `--explore-snr`.

---

## What SNR (dB) means in my noise test

SNR = Signal-to-Noise Ratio in decibels (dB).

Simple meaning:
- **Higher dB = cleaner audio**
- **Lower dB = more noise**

Levels I tested while choosing the pass gate:
- **20 dB:** mild background noise (often too easy for pass/fail)
- **15 dB:** moderate background noise (**official pass gate**)
- **10 dB:** heavier background noise (useful stress test, but harsh as the only gate)

Official pass gate uses **15 dB only**.

How I set it in code (`noise_utils.py`):
1. Measure speech power
2. Generate white noise
3. Scale noise to target power using  
   `SNR(dB) = 10 * log10(speech_power / noise_power)`

I use fixed random seed (`--noise-seed 42` default) so reruns are comparable.

---

## Test cases used

Source file:
- `for_reference/bhutan classifier test set.csv`

Filter:
- `in_scope = in_scope`
- `safety = safe`

Example utterances:
- "What papers I need for timber permit?"
- "Where is permit office in Thimphu?"
- "How to register business in Bhutan?"

---

## How I run

Run from **repo root** (`Voice-Team-C/`).

Setup:

```bash
pip install -r requirements.txt
```

Default pass-gate run (15 dB only, 10 utterances):

```bash
python team-c-voice/voice_assistant/asr_baseline/evaluate_asr_wer.py --limit 10 --whisper-model small
```

Exploratory multi-SNR run (20 / 15 / 10 dB — pass gate still 15 dB):

```bash
python team-c-voice/voice_assistant/asr_baseline/evaluate_asr_wer.py --limit 10 --explore-snr --whisper-model small
```

With clean reference:

```bash
python team-c-voice/voice_assistant/asr_baseline/evaluate_asr_wer.py --limit 10 --include-clean --whisper-model small
```

Full filtered set (official reported run):

```bash
python team-c-voice/voice_assistant/asr_baseline/evaluate_asr_wer.py --whisper-model small
```

---

## How I judge pass/fail

- **Pass gate:** mean WER < 0.20 at **15 dB SNR**
- **Exploration:** `--explore-snr` runs 20 / 15 / 10 dB for comparison (documented in `PROJECT_JOURNEY.md`)
- **Reference only:** clean WER (`--include-clean`)

---

## Current limitation (honest note)

Right now I generate test speech using gTTS for repeatability.  
This is a first baseline, but it is not the same as real human microphone speech.  
Next improvement: add recorded utterances for stronger validation.

---

## Outputs

- Audio: `voice_assistant/outputs/asr_baseline_audio/<timestamp>/`
- Report: `voice_assistant/outputs/asr_baseline_reports/asr_wer_results_<timestamp>.csv`

ffmpeg (or `imageio-ffmpeg`) is required for Whisper audio loading.
