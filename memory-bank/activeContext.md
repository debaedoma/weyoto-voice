# Active Context

## Current Focus
The high-converting all-in-one homepage for Weyoto Voice is complete and building successfully. The page includes everything needed for a user to generate TTS audio in one place.

## What Was Built
- **`lib/api.ts`** — API client with `fetchVoices()` and `generateVoice()` functions, auto-generates persistent user ID via `crypto.randomUUID()` in localStorage
- **`lib/constants.ts`** — Updated to match backend's `VOICE_CATALOG` (sigma_male, shes_her, lara_croft, british_prince) and `STYLE_MAP` (horror, story, funny, documentary, calm)
- **`components/home/voice-card.tsx`** — Selectable voice card with icon, label, description, selected state
- **`components/home/style-chips.tsx`** — Pill-style quick style selector (togglable)
- **`components/home/audio-result.tsx`** — Native `<audio>` player + Download MP3 button + word usage metadata
- **`components/home/voice-generator.tsx`** — Main Client Component with full form: textarea with live word counter (0/120), voice grid, style chips, custom fine-tune input, submit with loading spinner, error display, and result section
- **`components/home/hero-section.tsx`** — Compact hero with gradient background, badge, heading, description, scroll indicator
- **`src/app/page.tsx`** — Composes HeroSection + VoiceGenerator + FeaturesSection

## Key Design Decisions
- **Single-page app** — No separate /generate, /voices, or /about routes. Everything on `/`
- **Fine-tune overrides style** — Matching backend's `_resolve_instructions()` logic. Selecting a style clears fine-tune input, and typing a fine-tune clears the selected style
- **User ID** — Generated client-side via `crypto.randomUUID()`, persisted in localStorage
- **Server Components** — HeroSection and FeaturesSection are Server Components. Only VoiceGenerator (and its children VoiceCard, StyleChips, AudioResult) are Client Components
- **Mobile-first** — 2-col voice grid on mobile → 4-col on desktop. Full-width buttons on mobile → auto-width on desktop

## Build Status
- **Zero TypeScript errors** — strict mode with `noUncheckedIndexedAccess` passes cleanly
- Dev server runs on port 3001 (or 3002 if 3001 is taken)

## Next Steps
- Test full flow with Flask backend running
- Add voice preview playback (play sample before generating)
- Add user email capture for tracking
- Polish animations and transitions
- Deploy frontend (Vercel or similar)
