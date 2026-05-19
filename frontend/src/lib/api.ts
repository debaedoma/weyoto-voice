import { siteConfig } from "@/lib/constants";

export interface Voice {
  label: string;
  provider_voice: string;
  preview_url: string | null;
}

export interface VoicesResponse {
  status: string;
  voices: Record<string, Voice>;
}

export interface GenerateResponse {
  status: string;
  generation_id: string;
  audio_url: string;
  words_used: number;
  words_remaining: number;
  voice: string;
  provider_voice: string;
  instruction_source: string;
  created_at: string;
}

export interface GenerateError {
  status: "error" | "limit_reached";
  message: string;
  reset_in_days?: number;
}

export interface GeneratePayload {
  user_id: string;
  text: string;
  voice: string;
  style?: string;
  fine_tune?: string;
  email?: string;
}

function getApiUrl(): string {
  return siteConfig.apiUrl;
}

function getUserId(): string {
  // Use a simple localStorage-based user ID for MVP
  if (typeof window === "undefined") return "anonymous";

  let userId = localStorage.getItem("weyoto_user_id");
  if (!userId) {
    userId = crypto.randomUUID();
    localStorage.setItem("weyoto_user_id", userId);
  }
  return userId;
}

export async function fetchVoices(): Promise<VoicesResponse> {
  const response = await fetch(`${getApiUrl()}/voices`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch voices");
  }

  return response.json() as Promise<VoicesResponse>;
}

export async function generateVoice(
  payload: Omit<GeneratePayload, "user_id">,
): Promise<GenerateResponse> {
  const userId = getUserId();

  const response = await fetch(`${getApiUrl()}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ...payload,
      user_id: userId,
    }),
  });

  const data = (await response.json()) as GenerateResponse | GenerateError;

  if (!response.ok) {
    const errorData = data as GenerateError;
    throw new Error(errorData.message ?? "Unable to generate voice right now");
  }

  return data as GenerateResponse;
}

export function getAudioUrl(path: string): string {
  return `${getApiUrl()}${path}`;
}
