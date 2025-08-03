# 🧠 Weyoto Voice — Modular Flask App for Streaming AI Voice Generation

**Weyoto Voice** is a modular monolithic Flask application that streams realistic speech audio from OpenAI’s `gpt-4o-mini-tts` model. Built without a database for simplicity, it provides a pluggable, production-ready backend with a lightweight frontend interface for real-time AI voiceover generation.

---

## 🚀 Features

- 🔊 AI-generated speech using OpenAI's streaming TTS API
- 🧱 Modular monolithic Flask structure (easily extendable)
- 🎙️ Supports multiple OpenAI voices (Coral, River, Onyx, etc.)
- ✍️ Customizable tone using `instructions` (e.g., "speak confidently")
- 📁 Streams and saves MP3 audio files to disk
- 🧑‍💻 Web UI for text input, voice preview, and MP3 download
- ❌ No database required (stateless by design)

---

## 🧰 Tech Stack

| Layer        | Tech                       |
|--------------|----------------------------|
| Backend      | Flask (modular monolith)   |
| TTS Provider | OpenAI Python SDK (>=1.3)  |
| Frontend     | HTML + Vanilla JS          |
| Audio        | MP3 files streamed to disk |
| Hosting      | Render, Railway, or local  |
| Auth         | None (stateless MVP)       |

---

## 🧭 Project Structure

