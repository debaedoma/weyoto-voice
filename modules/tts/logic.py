import math
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from flask import current_app
from openai import OpenAI

from .store import (
    create_user,
    fetch_user,
    get_connection,
    increment_user_usage,
    record_generation,
    reset_user_weekly_usage,
    update_user_email,
)

client = OpenAI()  # Reads OPENAI_API_KEY from env

STYLE_MAP = {
    "horror": "Use a dark, suspenseful tone with slow pacing.",
    "story": "Narrate like a storyteller with smooth flow.",
    "funny": "Use a playful and comedic tone.",
    "documentary": "Use a calm, informative tone.",
    "calm": "Use a soft, relaxed tone.",
}

VOICE_CATALOG = {
    "sigma_male": {"label": "Sigma Male", "provider_voice": "ash"},
    "shes_her": {"label": "She's Her", "provider_voice": "coral"},
    "lara_croft": {"label": "Lara Croft", "provider_voice": "sage"},
    "british_prince": {"label": "British Prince", "provider_voice": "ballad"},
    "ballad_prince": {"label": "Ballad Prince", "provider_voice": "ballad"},
}

SUPPORTED_PROVIDER_VOICES = {
    "alloy",
    "ash",
    "ballad",
    "coral",
    "echo",
    "fable",
    "nova",
    "onyx",
    "river",
    "sage",
    "shimmer",
}


class GenerationValidationError(Exception):
    pass


class WeeklyLimitReachedError(Exception):
    def __init__(self, message, reset_in_days):
        super().__init__(message)
        self.reset_in_days = reset_in_days


def count_words(text):
    return len(text.split())


def list_available_voices():
    voices = {}

    for key, metadata in VOICE_CATALOG.items():
        preview_url = None
        preview_filename = f"previews/{key}.mp3"
        preview_path = Path(current_app.config["AUDIO_STORAGE_DIR"]) / preview_filename

        if preview_path.exists():
            preview_url = f"/audio/{preview_filename}"

        voices[key] = {
            "label": metadata["label"],
            "provider_voice": metadata["provider_voice"],
            "preview_url": preview_url,
        }

    return voices


def generate_voice_stream(text, voice, instructions, generation_id):
    filename = f"{generation_id}.mp3"
    output_dir = Path(current_app.config["AUDIO_STORAGE_DIR"])
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename

    with client.audio.speech.with_streaming_response.create(
        model=current_app.config["OPENAI_TTS_MODEL"],
        input=text,
        voice=voice,
        instructions=instructions,
    ) as response:
        response.stream_to_file(output_path)

    return filename


def process_generation_request(data):
    now = _get_current_time()
    created_at = now.isoformat()
    current_week_start = _get_week_start_date(now)

    user_id = _require_string(data.get("user_id"), "user_id is required")
    text = _require_string(data.get("text"), "Text is required")
    email = _optional_string(data.get("email"))
    style = _optional_string(data.get("style"))
    fine_tune = _optional_string(data.get("fine_tune"))

    requested_voice, provider_voice = _resolve_voice(data.get("voice"))
    word_count = count_words(text)
    max_words = current_app.config["MAX_WORDS_PER_GENERATION"]
    max_fine_tune_words = current_app.config["MAX_FINE_TUNE_WORDS"]

    if word_count == 0:
        raise GenerationValidationError("Text is required")

    if word_count > max_words:
        raise GenerationValidationError(f"Text exceeds {max_words} words")

    if fine_tune and count_words(fine_tune) > max_fine_tune_words:
        raise GenerationValidationError(
            f"Fine-tune cannot be more than {max_fine_tune_words} words"
        )

    # Fine-tune intentionally wins over style so the frontend can offer both inputs safely.
    instructions_used, instruction_source = _resolve_instructions(style, fine_tune)
    # Weekly limits are tracked against the current local Monday boundary.
    user = _load_user_for_current_week(user_id, email, current_week_start, created_at)

    weekly_limit = current_app.config["WEEKLY_WORD_LIMIT"]
    words_remaining_before = weekly_limit - user["words_used_this_week"]

    if word_count > words_remaining_before:
        raise WeeklyLimitReachedError(
            "Weekly word limit exceeded",
            _calculate_days_until_reset(now),
        )

    generation_id = str(uuid.uuid4())
    filename = generate_voice_stream(
        text=text,
        voice=provider_voice,
        instructions=instructions_used,
        generation_id=generation_id,
    )
    audio_url = f"/audio/{filename}"

    with get_connection() as connection:
        record_generation(
            connection=connection,
            generation_id=generation_id,
            user_id=user_id,
            text=text,
            requested_voice=requested_voice,
            provider_voice=provider_voice,
            style=style,
            fine_tune=fine_tune,
            instructions_used=instructions_used,
            word_count=word_count,
            audio_url=audio_url,
            created_at=created_at,
        )
        increment_user_usage(connection, user_id, word_count)
        connection.commit()

    words_remaining_after = words_remaining_before - word_count

    return {
        "status": "success",
        "generation_id": generation_id,
        "audio_url": audio_url,
        "words_used": word_count,
        "words_remaining": words_remaining_after,
        "voice": requested_voice,
        "provider_voice": provider_voice,
        "instruction_source": instruction_source,
        "created_at": created_at,
    }


def _load_user_for_current_week(user_id, email, week_start_date, created_at):
    with get_connection() as connection:
        user = fetch_user(connection, user_id)

        if not user:
            user = create_user(connection, user_id, email, week_start_date, created_at)
            connection.commit()
            return user

        # Reset usage the first time we see the user in a new local week.
        if user["week_start_date"] != week_start_date:
            reset_user_weekly_usage(connection, user_id, week_start_date)

        if email and email != user["email"]:
            update_user_email(connection, user_id, email)

        connection.commit()
        return fetch_user(connection, user_id)


def _resolve_voice(voice_value):
    voice = _require_string(voice_value, "Voice is required")
    normalized_voice = _normalize_lookup_value(voice)

    if normalized_voice in VOICE_CATALOG:
        return normalized_voice, VOICE_CATALOG[normalized_voice]["provider_voice"]

    if normalized_voice in SUPPORTED_PROVIDER_VOICES:
        return normalized_voice, normalized_voice

    raise GenerationValidationError("Selected voice is not supported")


def _resolve_instructions(style, fine_tune):
    if fine_tune:
        return fine_tune, "fine_tune"

    if style:
        normalized_style = _normalize_lookup_value(style)

        if normalized_style not in STYLE_MAP:
            raise GenerationValidationError("Selected style is not supported")

        return STYLE_MAP[normalized_style], "style"

    return current_app.config["DEFAULT_TTS_INSTRUCTION"], "default"


def _require_string(value, message):
    cleaned_value = _optional_string(value)

    if not cleaned_value:
        raise GenerationValidationError(message)

    return cleaned_value


def _optional_string(value):
    if value is None:
        return None

    cleaned_value = str(value).strip()
    return cleaned_value or None


def _normalize_lookup_value(value):
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def _get_current_time():
    return datetime.now(_get_app_timezone())


def _get_app_timezone():
    timezone_name = current_app.config["APP_TIMEZONE"]

    try:
        return ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError:
        # Lagos has a stable UTC+1 offset, so we can safely fall back for MVP.
        if timezone_name == "Africa/Lagos":
            return timezone(timedelta(hours=1), name="Africa/Lagos")

        return timezone.utc


def _get_week_start_date(current_time):
    monday = current_time - timedelta(days=current_time.weekday())
    return monday.date().isoformat()


def _calculate_days_until_reset(current_time):
    week_start = current_time - timedelta(days=current_time.weekday())
    next_week_start = week_start.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    ) + timedelta(days=7)
    return max(0, math.ceil((next_week_start - current_time).total_seconds() / 86400))
