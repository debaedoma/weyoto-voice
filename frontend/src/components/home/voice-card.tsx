"use client";

import { cn } from "@/lib/utils";

interface VoiceCardProps {
  voiceKey: string;
  label: string;
  description: string;
  icon: string;
  isSelected: boolean;
  onSelect: () => void;
}

export function VoiceCard({
  voiceKey,
  label,
  description,
  icon,
  isSelected,
  onSelect,
}: VoiceCardProps) {
  return (
    <button
      type="button"
      onClick={onSelect}
      className={cn(
        "flex flex-col items-center gap-1.5 rounded-xl border-2 p-3 text-center transition-all duration-150 sm:p-4",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
        isSelected
          ? "border-primary bg-primary/5 shadow-sm"
          : "border-border bg-card hover:border-muted-foreground/30 hover:bg-muted/30",
      )}
      aria-pressed={isSelected}
      aria-label={`Select ${label} voice`}
    >
      <span className="text-2xl sm:text-3xl" aria-hidden="true">
        {icon}
      </span>
      <span
        className={cn(
          "text-xs font-semibold sm:text-sm",
          isSelected ? "text-primary" : "text-foreground",
        )}
      >
        {label}
      </span>
      <span className="text-[10px] leading-tight text-muted-foreground sm:text-xs">
        {description}
      </span>
    </button>
  );
}
