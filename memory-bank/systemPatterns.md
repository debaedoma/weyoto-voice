# System Patterns & Architecture

## Overall Architecture
```
weyoto-voice/
├── app.py                    # Flask application entry point
├── config.py                 # Configuration
├── extensions.py             # Flask extensions
├── modules/
│   └── tts/                  # TTS module (routes + logic)
├── frontend/                 # Next.js 15+ frontend (separate)
├── tests/                    # Backend tests
├── utils/                    # Utility modules
└── memory-bank/              # Project documentation
```

## Frontend Architecture (Next.js 15+)

### Component Hierarchy
```
RootLayout (Server)
├── Navbar (Client - needs useState for mobile menu)
├── <main>
│   └── Page Content (Server)
│       ├── HeroSection (Server)
│       └── FeaturesSection (Server)
└── Footer (Server)
```

### Design Patterns
- **Server Components by default**: All data fetching and rendering happens on the server
- **Client Components only at leaf nodes**: Only `navbar.tsx` is a Client Component (for interactivity)
- **Mobile-first responsive**: All layouts use Tailwind's `sm:`, `md:`, `lg:` breakpoints
- **Shadcn UI**: Component library built on Radix UI primitives with Tailwind styling

### Directory Structure
```
frontend/src/
├── app/           # App Router pages and layouts
├── components/
│   ├── ui/        # Shadcn UI primitives (Button, Card, Sheet)
│   ├── layout/    # Layout components (Navbar, Footer)
│   └── home/      # Home page components (Hero, Features)
├── lib/           # Utilities and constants
└── hooks/         # Custom React hooks
```

## Backend Architecture (Flask)
- Modular monolithic structure
- TTS logic separated into `modules/tts/logic.py`
- API routes in `modules/tts/routes.py`
- SQLite database (optional, MVP-friendly)
