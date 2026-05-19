# Technical Context

## Technologies Used

### Frontend
- **Next.js 16.2.6** (App Router) — React framework with server components
- **React 19.2.4** — UI library
- **TypeScript 5.x** — Strict type safety
- **Tailwind CSS v4** — Utility-first CSS framework
- **Shadcn UI** — Component library (Button, Card, Sheet)
- **Lucide React** — Icon library
- **@base-ui/react** — Headless UI primitives used by Shadcn

### Backend
- **Python 3.x** — Runtime
- **Flask** — Web framework
- **OpenAI API** — TTS generation via `gpt-4o-mini-tts`

## Development Setup

### Frontend
```bash
cd frontend
npm install
npm run dev        # http://localhost:3000
```

### Backend
```bash
python -m venv venv
pip install -r requirements.txt
export OPENAI_API_KEY=your-key
python app.py      # http://localhost:5000
```

## Key Dependencies (Frontend)
- `next`, `react`, `react-dom` — Core framework
- `tailwindcss`, `@tailwindcss/postcss` — Styling
- `class-variance-authority` — Component variants
- `clsx`, `tailwind-merge` — Class name utilities
- `lucide-react` — Icons
- `tw-animate-css` — Animation utilities

## Environment Variables
- `NEXT_PUBLIC_API_URL` — Backend API URL (default: `http://localhost:5000`)

## Constraints
- No `any` types allowed in TypeScript
- Mobile-first responsive design required
- Server Components preferred over Client Components
- Frontend must be fully independent from backend code
