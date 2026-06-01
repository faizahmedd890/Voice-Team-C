# Voice-Team-C

Bhutan public-service voice work (Team C).

## Docs and run commands

| Folder | Entry doc |
|---|---|
| Sprint 1 TTS (gTTS vs Coqui) | [`team-c-voice/tts/README.md`](team-c-voice/tts/README.md) |
| Sprint 2 voice assistant + ASR baseline | [`team-c-voice/voice_assistant/README.md`](team-c-voice/voice_assistant/README.md) |

Setup for both: from this repo root, `pip install -r requirements.txt`

Voice assistant also needs `GROQ_API_KEY` in repo-root `.env` (copy from `.env.example`, add your key; `.env` is not committed).
