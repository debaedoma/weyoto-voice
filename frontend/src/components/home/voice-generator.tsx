"use client";

import { useState, type FormEvent, type KeyboardEvent } from "react";
import { Loader2, Sparkles } from "lucide-react";

import { Button } from "@/components/ui/button";
import { VoiceCard } from "@/components/home/voice-card";
import { StyleChips } from "@/components/home/style-chips";
import { AudioResult } from "@/components/home/audio-result";
import {
  voiceCatalog,
  voiceKeys,
  MAX_WORDS,
  MAX_FINE_TUNE_WORDS,
} from "@/lib/constants";
import { generateVoice } from "@/lib/api";
import type { GenerateResponse } from "@/lib/api";
import { cn } from "@/lib/utils";

export function VoiceGenerator() {
  const [text, setText] = useState("");
  const [selectedVoice, setSelectedVoice] = useState<string | null>(null);
  const [selectedStyle, setSelectedStyle] = useState<string | null>(null);
  const [fineTune, setFineTune] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<GenerateResponse | null>(null);

  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const isOverLimit = wordCount > MAX_WORDS;
  const hasText = text.trim().length > 0;
  const canGenerate =
    hasText && selectedVoice !== null && !isOverLimit && !isGenerating;

  const doGenerate = async (): Promise<void> => {
    if (!canGenerate || !selectedVoice) return;

    setIsGenerating(true);
    setError(null);
    setResult(null);

    try {
      const payload: {
        text: string;
        voice: string;
        style?: string;
        fine_tune?: string;
      } = {
        text: text.trim(),
        voice: selectedVoice,
      };

      // Fine-tune wins over style (matching backend logic)
      if (fineTune.trim()) {
        payload.fine_tune = fineTune.trim();
      } else if (selectedStyle) {
        payload.style = selectedStyle;
      }

      const response = await generateVoice(payload);
      setResult(response);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to generate voice right now",
      );
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSubmit = (e: FormEvent): void => {
    e.preventDefault();
    doGenerate();
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>): void => {
    // Submit on Ctrl+Enter or Cmd+Enter
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      doGenerate();
    }
  };

  const handleStyleSelect = (styleKey: string | null): void => {
    setSelectedStyle(styleKey);
    if (styleKey) {
      setFineTune("");
    }
  };

  const handleFineTuneChange = (value: string): void => {
    setFineTune(value);
    if (value.trim()) {
      setSelectedStyle(null);
    }
  };

  return (
    <section className="px-4 pb-16 sm:px-6 sm:pb-20 lg:pb-24">
      <div className="mx-auto max-w-3xl">
        {/* Text Input */}
        <div className="mb-6 sm:mb-8">
          <label
            htmlFor="tts-text"
            className="mb-2 block text-sm font-medium text-foreground"
          >
            Your Text
          </label>
          <textarea
            id="tts-text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type or paste your text here... e.g. 'The sailor was sailing at night and the waves were blowing hard.'"
            rows={4}
            className={cn(
              "w-full resize-none rounded-xl border-2 bg-card p-4 text-sm transition-all duration-150 placeholder:text-muted-foreground/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-1 sm:text-base",
              isOverLimit
                ? "border-destructive"
                : "border-border focus-visible:border-primary",
            )}
            aria-describedby="word-count"
          />
          <div
            id="word-count"
            className={cn(
              "mt-1.5 text-xs tabular-nums",
              isOverLimit
                ? "font-medium text-destructive"
                : "text-muted-foreground",
            )}
          >
            {wordCount} / {MAX_WORDS} words
            {isOverLimit && " — Text exceeds the word limit"}
          </div>
        </div>

        {/* Voice Selection */}
        <div className="mb-6 sm:mb-8">
          <label className="mb-3 block text-sm font-medium text-foreground">
            Choose a Voice
          </label>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 sm:gap-4">
            {voiceKeys.map((key) => {
              const voice = voiceCatalog[key];
              if (!voice) return null;
              return (
                <VoiceCard
                  key={key}
                  voiceKey={key}
                  label={voice.label}
                  description={voice.description}
                  icon={voice.icon}
                  isSelected={selectedVoice === key}
                  onSelect={() => setSelectedVoice(key)}
                />
              );
            })}
          </div>
        </div>

        {/* Style / Fine-Tune */}
        <div className="mb-6 sm:mb-8">
          <label className="mb-3 block text-sm font-medium text-foreground">
            Tone <span className="text-muted-foreground">(optional)</span>
          </label>

          {/* Quick Styles */}
          <div className="mb-3">
            <p className="mb-2 text-xs text-muted-foreground">Quick styles:</p>
            <StyleChips
              selectedStyle={selectedStyle}
              onSelect={handleStyleSelect}
            />
          </div>

          {/* Divider */}
          <div className="relative mb-3">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t border-border" />
            </div>
            <div className="relative flex justify-center">
              <span className="bg-background px-2 text-xs text-muted-foreground">
                or custom instruction
              </span>
            </div>
          </div>

          {/* Custom Fine-Tune */}
          <div>
            <input
              id="tts-fine-tune"
              type="text"
              value={fineTune}
              onChange={(e) => handleFineTuneChange(e.target.value)}
              placeholder='e.g. "Sound terrifying" or "Speak like a wise old wizard"'
              className={cn(
                "w-full rounded-xl border-2 bg-card px-4 py-2.5 text-sm transition-all duration-150 placeholder:text-muted-foreground/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-1 sm:text-base",
                fineTune.trim().length > MAX_FINE_TUNE_WORDS
                  ? "border-destructive"
                  : "border-border focus-visible:border-primary",
              )}
            />
            <p className="mt-1 text-xs text-muted-foreground">
              Max {MAX_FINE_TUNE_WORDS} words. Overrides the quick style above.
            </p>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div
            role="alert"
            className="mb-6 rounded-xl border border-destructive/30 bg-destructive/5 px-4 py-3 text-sm text-destructive sm:mb-8"
          >
            {error}
          </div>
        )}

        {/* Submit Button */}
        <form onSubmit={handleSubmit}>
          <Button
            type="submit"
            size="lg"
            disabled={!canGenerate}
            className="w-full gap-2 text-base sm:text-lg"
          >
            {isGenerating ? (
              <>
                <Loader2 className="size-5 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Sparkles className="size-5" />
                Generate Voice
              </>
            )}
          </Button>
        </form>

        {/* Result */}
        {result && (
          <div className="mt-6 sm:mt-8">
            <AudioResult result={result} />
          </div>
        )}
      </div>
    </section>
  );
}
