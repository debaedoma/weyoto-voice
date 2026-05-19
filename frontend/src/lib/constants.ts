export const siteConfig = {
  name: "Weyoto Voice",
  tagline: "Your words. A new voice.",
  description:
    "AI-powered text-to-speech generator that turns your text into high-quality, realistic speech using OpenAI's advanced TTS models.",
  url: "https://voice.weyoto.com",
  apiUrl: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:5000",
} as const;

export const navLinks = [
  { label: "Home", href: "/" },
] as const;

/**
 * Matches the backend VOICE_CATALOG in modules/tts/logic.py
 */
export const voiceCatalog: Record<
  string,
  { label: string; providerVoice: string; description: string; icon: string }
> = {
  sigma_male: {
    label: "Sigma Male",
    providerVoice: "ash",
    description: "Deep, confident, and commanding",
    icon: "🎙️",
  },
  shes_her: {
    label: "She's Her",
    providerVoice: "coral",
    description: "Warm, friendly, and approachable",
    icon: "🎤",
  },
  lara_croft: {
    label: "Lara Croft",
    providerVoice: "sage",
    description: "Adventurous, bold, and articulate",
    icon: "🗣️",
  },
  british_prince: {
    label: "British Prince",
    providerVoice: "ballad",
    description: "Refined, elegant, and poised",
    icon: "👑",
  },
} as const;

export const voiceKeys = Object.keys(voiceCatalog) as Array<
  keyof typeof voiceCatalog
>;

/**
 * Matches the backend STYLE_MAP in modules/tts/logic.py
 */
export const styleOptions = [
  { key: "horror", label: "Horror", description: "Dark & suspenseful" },
  { key: "story", label: "Story", description: "Storyteller narration" },
  { key: "funny", label: "Funny", description: "Playful & comedic" },
  {
    key: "documentary",
    label: "Documentary",
    description: "Calm & informative",
  },
  { key: "calm", label: "Calm", description: "Soft & relaxed" },
] as const;

export const features = [
  {
    title: "AI-Powered TTS",
    description:
      "Leverage OpenAI's gpt-4o-mini-tts model for natural, human-like speech synthesis.",
    icon: "🎤",
  },
  {
    title: "Tone Customization",
    description:
      "Fine-tune the emotional tone with natural language instructions like 'sound terrifying' or 'speak softly'.",
    icon: "🎨",
  },
  {
    title: "Multiple Voices",
    description:
      "Choose from 4 distinct voices, each with its own unique personality and style.",
    icon: "🗣️",
  },
  {
    title: "Fast Generation",
    description:
      "Streaming audio generation delivers your speech in seconds, not minutes.",
    icon: "⚡",
  },
  {
    title: "Downloadable MP3",
    description:
      "Export your generated speech as high-quality MP3 files ready for use.",
    icon: "📥",
  },
  {
    title: "No Setup Required",
    description:
      "Start generating immediately — no microphone, no editing, no complex configuration.",
    icon: "🚀",
  },
] as const;

export const MAX_WORDS = 120;
export const MAX_FINE_TUNE_WORDS = 25;
