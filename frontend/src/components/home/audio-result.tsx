"use client";

import { useRef } from "react";
import { Download, Play, Pause } from "lucide-react";

import { Button } from "@/components/ui/button";
import { getAudioUrl } from "@/lib/api";
import type { GenerateResponse } from "@/lib/api";

interface AudioResultProps {
  result: GenerateResponse;
}

export function AudioResult({ result }: AudioResultProps) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const audioUrl = getAudioUrl(result.audio_url);

  const handleDownload = (): void => {
    const link = document.createElement("a");
    link.href = audioUrl;
    link.download = `weyoto-${result.generation_id}.mp3`;
    link.click();
  };

  return (
    <div className="rounded-xl border border-border bg-card p-4 sm:p-6">
      <h3 className="mb-3 text-sm font-semibold text-foreground sm:text-base">
        Your Voice is Ready ✨
      </h3>

      {/* Audio Player */}
      <div className="mb-4 flex items-center gap-3 rounded-lg bg-muted/50 p-3">
        <audio
          ref={audioRef}
          src={audioUrl}
          controls
          className="h-10 w-full"
          preload="metadata"
        >
          Your browser does not support the audio element.
        </audio>
      </div>

      {/* Meta + Download */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="space-y-1 text-xs text-muted-foreground sm:text-sm">
          <p>
            Voice: <span className="font-medium text-foreground">{result.voice}</span>
          </p>
          <p>
            Words used:{" "}
            <span className="font-medium text-foreground">
              {result.words_used}
            </span>
            {" · "}
            Remaining:{" "}
            <span className="font-medium text-foreground">
              {result.words_remaining}
            </span>
          </p>
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={handleDownload}
          className="w-full gap-2 sm:w-auto"
        >
          <Download className="size-4" />
          Download MP3
        </Button>
      </div>
    </div>
  );
}
