"use client";

import { cn } from "@/lib/utils";
import { styleOptions } from "@/lib/constants";

interface StyleChipsProps {
  selectedStyle: string | null;
  onSelect: (styleKey: string | null) => void;
}

export function StyleChips({ selectedStyle, onSelect }: StyleChipsProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {styleOptions.map((style) => (
        <button
          key={style.key}
          type="button"
          onClick={() =>
            onSelect(selectedStyle === style.key ? null : style.key)
          }
          className={cn(
            "rounded-full border px-3 py-1.5 text-xs font-medium transition-all duration-150 sm:text-sm",
            "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-1",
            selectedStyle === style.key
              ? "border-primary bg-primary text-primary-foreground"
              : "border-border bg-card text-muted-foreground hover:border-muted-foreground/30 hover:text-foreground",
          )}
          aria-pressed={selectedStyle === style.key}
          aria-label={`Select ${style.label} style`}
        >
          {style.label}
        </button>
      ))}
    </div>
  );
}
