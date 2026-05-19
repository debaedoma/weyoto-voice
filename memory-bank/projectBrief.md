# Weyoto Voice — Project Brief

## Overview
Weyoto Voice is an AI-powered Text-to-Speech generator that converts text into high-quality, realistic speech using OpenAI's `gpt-4o-mini-tts` model. Users can customize tone using natural language instructions and generate downloadable MP3s instantly.

## Core Requirements
- **Backend**: Modular Flask application with TTS generation logic and REST API
- **Frontend**: Modern Next.js 15+ application with App Router, TypeScript, Tailwind CSS, and Shadcn UI
- **Separation**: Frontend lives in `frontend/` folder, completely independent from backend
- **Mobile-first**: All UI components must be fully responsive using Tailwind breakpoints

## Key Features
- AI-powered text-to-speech via OpenAI streaming TTS API
- Tone customization via natural language instructions
- 8 distinct voices (Coral, River, Shimmer, Echo, Nova, Onyx, Fable, Alloy)
- Fast streaming audio generation
- Downloadable MP3 output
- Modular monolithic Flask structure (backend)

## Goals
- Provide a clean, professional UI for the TTS service
- Prioritize Server Components for data fetching
- Use Client Components only at leaf nodes for interactivity
- Maintain strict TypeScript safety (no `any` types)
- Ensure flawless responsive design from mobile to desktop
