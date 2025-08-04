# 🖙️ Weyoto Voice — AI-Powered Text-to-Speech Generator (Flask + OpenAI)

**Weyoto Voice** is a modular Flask application that turns text into high-quality, realistic speech using OpenAI’s `gpt-4o-mini-tts` model. Users can customize tone using natural language instructions and generate downloadable MP3s in seconds — no microphone, no editing.

Built with a clean monolithic structure (no database), this is a perfect starter project or production-ready base for voice automation, storytelling tools, or creative audio projects.

---

## ✨ Features

* 🎤 AI-powered text-to-speech using OpenAI's streaming TTS API
* 🧠 Tone customization via natural instructions (e.g., “sound terrifying”)
* 🎧 Multiple voices: Coral, River, Shimmer, Onyx, etc.
* ⚡ Fast streaming audio generation
* 📅 Saves output as `.mp3` files in `static/audio/`
* 🧱 Modular monolithic Flask structure
* 🔓 No database or auth required (MVP-friendly)
* 🧑‍💻 Simple HTML + JS frontend # Update

---

## 🧱 Project Structure

```
weyoto-voice/
├── app.py
├── config.py
├── extensions.py
├── modules/
│   └── tts/
│       ├── __init__.py
│       ├── logic.py          # TTS generation logic
│       ├── routes.py         # Flask routes for UI & API
│       └── templates/
│           └── index.html    # Basic frontend UI
├── app/
│   └── static/  
            └── audio/       # Saved MP3 files
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🧑‍💻 Getting Started

### 1. Clone and Set Up Environment

```bash
git clone https://github.com/your-username/weyoto-voice.git
cd weyoto-voice
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Set Your OpenAI API Key

```bash
export OPENAI_API_KEY=your-openai-key  # macOS/Linux
# OR
$env:OPENAI_API_KEY="your-openai-key"  # Windows PowerShell
```

### 3. Run the App

```bash
python app.py
```

Visit `http://localhost:5000/tts` in your browser.

---

## 📄 API Example (Postman or JS)

**POST** `/tts/generate-voice`
Content-Type: `application/json`

```json
{
  "text": "The sailor was sailing at night and the waves were blowing hard. He decided to stop and not sail for the night",
  "voice": "coral",
  "instructions": "The voice should sound terrifying"
}
```

Response: downloadable MP3 file of the voiceover.

---

## 🔊 Available Voices

| Voice     | Style                |
| --------- | -------------------- |
| `coral`   | Calm and friendly    |
| `river`   | Confident and bold   |
| `shimmer` | Soft and soothing    |
| `echo`    | Crisp and clear      |
| `nova`    | Bright and energetic |
| `onyx`    | Deep and bold        |
| `fable`   | Storytelling tone    |
| `alloy`   | Balanced neutral     |

---

## 📦 Deployment Notes

* Compatible with [Render](https://render.com), [Railway](https://railway.app), or any VPS
* MP3 files are stored locally in `static/audio/` — consider cleanup or time-based deletion
* Optional enhancements include:

  * Adding Tailwind for styling
  * Integrating with Wasabi/S3 for permanent storage
  * Adding auth or usage tracking later

---

## 🧳 Roadmap Ideas

* [ ] Auto-delete old audio files after 10 minutes
* [ ] Add reusable voice templates (presets)
* [ ] Add background music overlays
* [ ] Deploy at `voice.weyoto.com`
* [ ] Add Stripe/Paystack billing for pro usage
* [ ] Support streaming playback without saving

---

## 📄 License

MIT License — free to use, extend, or commercialize.

---

## 👋 Author

Built with love by Deba, creator of Weyoto and builder of AI tools that actually work.
For contributions or feedback, open an issue or pull request.

---

> 🧠 “Your words. A new voice.” — [Weyoto Voice](https://voice.weyoto.com)

```
```
