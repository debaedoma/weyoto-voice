"use client";

import { useEffect, useState } from "react";

/**
 * Custom hook that tracks whether a CSS media query matches.
 * Useful for responsive behavior in client components.
 *
 * @param query - The CSS media query string to evaluate.
 * @returns `true` if the media query matches, `false` otherwise.
 */
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState<boolean>(false);

  useEffect(() => {
    const mediaQueryList = window.matchMedia(query);

    // Set initial value
    setMatches(mediaQueryList.matches);

    // Update matches when the viewport changes
    const handleChange = (event: MediaQueryListEvent): void => {
      setMatches(event.matches);
    };

    mediaQueryList.addEventListener("change", handleChange);

    return () => {
      mediaQueryList.removeEventListener("change", handleChange);
    };
  }, [query]);

  return matches;
}

/**
 * Predefined breakpoint hooks for common Tailwind breakpoints.
 */
export function useIsSm(): boolean {
  return useMediaQuery("(min-width: 640px)");
}

export function useIsMd(): boolean {
  return useMediaQuery("(min-width: 768px)");
}

export function useIsLg(): boolean {
  return useMediaQuery("(min-width: 1024px)");
}

export function useIsXl(): boolean {
  return useMediaQuery("(min-width: 1280px)");
}
