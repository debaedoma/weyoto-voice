# 🖙️ Weyoto Voice — AI-Powered Text-to-Speech Generator (Flask + Next.js)

**Weyoto Voice** is a full-stack application that turns text into high-quality, realistic speech using OpenAI's `gpt-4o-mini-tts` model. Users can choose from 4 distinct branded voices, customize tone with natural language instructions or preset styles, and generate downloadable MP3s in seconds — no microphone, no editing.

Built with a modular Flask backend and a modern Next.js frontend, this is a production-ready base for voice automation, storytelling tools, or creative audio projects.

---

## ✨ Features

- 🎤 **AI-powered TTS** — Uses OpenAI's streaming TTS API (`gpt-4o-mini-tts`)
- 🗣️ **4 Branded Voices** — Sigma Male, She's Her, Lara Croft, British Prince
- 🎨 **Tone Customization** — Choose from 5 preset styles (Horror, Story, Funny, Documentary, Calm) or write your own fine-tune instructions
- ⚡ **Fast Streaming Generation** — Audio generated and ready in seconds
- 📥 **Downloadable MP3** — Save generated speech as high-quality MP3 files
- 👤 **User Tracking** — Anonymous user IDs with weekly word limits (500 words/week default)
- 🗄️ **SQLite Database** — Tracks usage, generations, and user limits
- 🧪 **Tested Backend** — Pytest test suite for routes and logic
- 🧱 **Modular Architecture** — Clean separation between backend (Flask) and frontend (Next.js)

---

## 🧱 Project Structure

```
weyoto-voice/
├── app.py                    # Flask application entry point
├── config.py                 # Configuration & environment variables
├── extensions.py             # Flask extensions
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API key, settings)
├── .gitignore
├── README.md
│
├── modules/
│   └── tts/                  # TTS module
│       ├── __init__.py
│       ├── logic.py          # TTS generation logic, validation, voice catalog
│       ├── routes.py         # Flask API routes (/generate, /voices, /audio)
│       ├── store.py          # SQLite database operations
│       └── templates/
│           └── index.html    # Legacy Flask frontend
│
├── frontend/                 # Next.js 16 frontend (separate app)
│   ├── src/
│   │   ├── app/              # App Router pages & layouts
│   │   ├── components/
│   │   │   ├── ui/           # Shadcn UI primitives (Button, Card, Sheet)
│   │   │   ├── layout/       # Navbar, Footer
│   │   │   └── home/         # HeroSection, VoiceGenerator, VoiceCard, etc.
│   │   ├── lib/              # API client, constants, utilities
│   │   └── hooks/            # Custom React hooks
│   ├── package.json
│   └── tsconfig.json
│
├── tests/                    # Backend test suite
│   ├── conftest.py           # Pytest fixtures
│   ├── test_logic.py         # Tests for TTS logic
│   └── test_routes.py        # Tests for API routes
│
├── instance/
│   ├── audio/                # Generated MP3 files (runtime only)
│   │   └── previews/         # Voice preview MP3 files
│   └── weyoto_voice.db       # SQLite database (auto-created)
│
├── utils/                    # Utility modules
└── memory-bank/              # Project documentation (Claude context)
```

---

## 🧑‍💻 Getting Started

### Prerequisites

- Python 3.x
- Node.js 18+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 1. Clone and Set Up Backend

```bash
git clone https://github.com/your-username/weyoto-voice.git
cd weyoto-voice
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-openai-key
DEBUG=True
APP_TIMEZONE=Africa/Lagos
WEEKLY_WORD_LIMIT=500
MAX_WORDS_PER_GENERATION=120
MAX_FINE_TUNE_WORDS=25
```

### 3. Run the Backend

```bash
python app.py
```

The Flask API will be available at `http://localhost:5000`.

### 4. Set Up and Run the Frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

The Next.js frontend will be available at `http://localhost:3000` (or 3001 if taken).

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

---

## 📄 API Reference

### `GET /voices`

Returns the list of available voices with preview URLs.

**Response:**
```json
{
  "status": "success",
  "voices": {
    "sigma_male": {
      "label": "Sigma Male",
      "provider_voice": "ash",
      "preview_url": "/audio/previews/sigma_male.mp3"
    },
    "shes_her": { "label": "She's Her", "provider_voice": "coral", "preview_url": null },
    "lara_croft": { "label": "Lara Croft", "provider_voice": "sage", "preview_url": null },
    "british_prince": { "label": "British Prince", "provider_voice": "ballad", "preview_url": null }
  }
}
```

### `POST /generate` (or `/generate-voice` or `/tts/generate-voice`)

Generates speech from text.

**Request:**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "text": "The sailor was sailing at night and the waves were blowing hard.",
  "voice": "sigma_male",
  "style": "story",
  "fine_tune": "Speak with a mysterious, hushed tone",
  "email": "user@example.com"
}
```

| Field       | Type   | Required | Description |
|-------------|--------|----------|-------------|
| `user_id`   | string | ✅       | UUID for anonymous user tracking |
| `text`      | string | ✅       | Text to convert (max 120 words) |
| `voice`     | string | ✅       | Voice key from `/voices` |
| `style`     | string | ❌       | Preset style key (horror, story, funny, documentary, calm) |
| `fine_tune` | string | ❌       | Custom tone instructions (max 25 words, overrides style) |
| `email`     | string | ❌       | Optional email for user tracking |

**Response (201):**
```json
{
  "status": "success",
  "generation_id": "0ff6f486-2f18-4d70-9e57-a1b4df4b5537",
  "audio_url": "/audio/0ff6f486-2f18-4d70-9e57-a1b4df4b5537.mp3",
  "words_used": 14,
  "words_remaining": 486,
  "voice": "sigma_male",
  "provider_voice": "ash",
  "instruction_source": "style",
  "created_at": "2026-05-19T22:35:30+01:00"
}
```

**Error Responses:**
- `400` — Validation error (missing fields, word limit exceeded, unsupported voice/style)
- `429` — Weekly word limit reached (includes `reset_in_days`)
- `500` — Internal server error

### `GET /audio/<filename>`

Serves a generated MP3 file for download or playback.

---

## 🔊 Available Voices

| Key              | Label           | Provider Voice | Style                |
| ---------------- | --------------- | -------------- | -------------------- |
| `sigma_male`     | Sigma Male      | `ash`          | Deep, confident      |
| `shes_her`       | She's Her       | `coral`        | Warm, friendly       |
| `lara_croft`     | Lara Croft      | `sage`         | Adventurous, bold    |
| `british_prince` | British Prince  | `ballad`       | Refined, elegant     |

### 🎨 Preset Styles

| Key            | Description                |
| -------------- | -------------------------- |
| `horror`       | Dark & suspenseful         |
| `story`        | Storyteller narration      |
| `funny`        | Playful & comedic          |
| `documentary`  | Calm & informative         |
| `calm`         | Soft & relaxed             |

> **Note:** Fine-tune instructions override preset styles. Selecting a style clears any custom fine-tune, and typing a fine-tune clears the selected style.

---

## ⚙️ Configuration

All settings are configured via environment variables in `.env`:

| Variable                   | Default                  | Description |
|----------------------------|--------------------------|-------------|
| `OPENAI_API_KEY`           | —                        | Your OpenAI API key |
| `DEBUG`                    | `False`                  | Enable Flask debug mode |
| `APP_TIMEZONE`             | `Africa/Lagos`           | Timezone for weekly resets |
| `OPENAI_TTS_MODEL`         | `gpt-4o-mini-tts`        | OpenAI TTS model ID |
| `WEEKLY_WORD_LIMIT`        | `500`                    | Max words per user per week |
| `MAX_WORDS_PER_GENERATION` | `120`                    | Max words per request |
| `MAX_FINE_TUNE_WORDS`      | `25`                     | Max words for fine-tune instructions |
| `DEFAULT_TTS_INSTRUCTION`  | `Match the tone of the text.` | Default TTS instruction |
| `DATABASE_PATH`            | `instance/weyoto_voice.db` | SQLite database path |
| `AUDIO_STORAGE_DIR`        | `instance/audio`         | MP3 output directory |

---

## 🧪 Running Tests

```bash
# From the project root (with venv activated)
pytest tests/ -v
```

---

## 📦 Deployment Notes

- **Backend**: Compatible with [Render](https://render.com), [Railway](https://railway.app), or any VPS
- **Frontend**: Deploy to [Vercel](https://vercel.com) for optimal Next.js support
- MP3 files are stored locally in `instance/audio/` — consider cleanup or cloud storage (S3/Wasabi) for production
- The SQLite database is local — consider PostgreSQL for multi-instance deployments

---

## 🧳 Roadmap

- [ ] Voice preview playback (play sample before generating)
- [ ] Auto-delete old audio files after 10 minutes
- [ ] Reusable voice templates (presets)
- [ ] Background music overlays
- [ ] Deploy at `voice.weyoto.com`
- [ ] Stripe/Paystack billing for pro usage
- [ ] Streaming playback without saving
- [ ] User email capture for analytics
- [ ] Polish animations and transitions

---

## 📄 License

MIT License — free to use, extend, or commercialize.

---

## 👋 Author

Built with love by Deba, creator of Weyoto and builder of AI tools that actually work.
For contributions or feedback, open an issue or pull request.

---

> 🧠 *"Your words. A new voice."* — [Weyoto Voice](https://voice.weyoto.com)
