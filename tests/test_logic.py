"""
test_logic.py — Unit tests for the core logic functions.

These tests check the "pure" functions in logic.py — functions that
take inputs and return outputs without needing a database or Flask app.

What we're testing:
  - count_words: Word counting
  - _normalize_lookup_value: Voice/style name normalization
  - _optional_string / _require_string: Input cleaning and validation
  - _resolve_voice: Voice lookup logic
  - _resolve_instructions: Style/fine-tune resolution
  - _get_week_start_date: Weekly boundary calculation
  - _calculate_days_until_reset: Time-until-reset calculation

Why no Flask app needed?
    These functions either:
    - Don't use current_app at all, OR
    - We pass them the values they need directly
"""

from datetime import datetime, timedelta, timezone

import pytest

from modules.tts.logic import (
    GenerationValidationError,
    count_words,
    _normalize_lookup_value,
    _optional_string,
    _require_string,
    _resolve_voice,
    _resolve_instructions,
    _get_week_start_date,
    _calculate_days_until_reset,
)


# ─── count_words ────────────────────────────────────────────────────

class TestCountWords:
    """Tests for the count_words function."""

    def test_empty_string(self):
        """An empty string should have 0 words."""
        assert count_words("") == 0

    def test_single_word(self):
        """A single word should count as 1."""
        assert count_words("Hello") == 1

    def test_multiple_words(self):
        """Multiple words separated by spaces should be counted correctly."""
        assert count_words("Hello world this is a test") == 6

    def test_extra_spaces(self):
        """Extra spaces between words should not affect the count."""
        assert count_words("Hello    world") == 2

    def test_leading_trailing_spaces(self):
        """Leading and trailing spaces should be ignored."""
        assert count_words("   Hello world   ") == 2


# ─── _normalize_lookup_value ────────────────────────────────────────

class TestNormalizeLookupValue:
    """Tests for the _normalize_lookup_value function.

    This function converts user-friendly names like "Sigma Male"
    into internal keys like "sigma_male" by:
    - Lowercasing
    - Replacing spaces and hyphens with underscores
    - Stripping whitespace
    """

    def test_lowercases(self):
        """Input should be converted to lowercase."""
        assert _normalize_lookup_value("SIGMA_MALE") == "sigma_male"

    def test_replaces_spaces_with_underscores(self):
        """Spaces should become underscores."""
        assert _normalize_lookup_value("sigma male") == "sigma_male"

    def test_replaces_hyphens_with_underscores(self):
        """Hyphens should become underscores."""
        assert _normalize_lookup_value("sigma-male") == "sigma_male"

    def test_strips_whitespace(self):
        """Leading/trailing whitespace should be removed."""
        assert _normalize_lookup_value("  sigma_male  ") == "sigma_male"

    def test_handles_mixed_separators(self):
        """Mixed spaces, hyphens, and underscores should all normalize."""
        assert _normalize_lookup_value("British Prince") == "british_prince"


# ─── _optional_string ───────────────────────────────────────────────

class TestOptionalString:
    """Tests for the _optional_string helper.

    This function cleans a value:
    - None → None
    - Empty/whitespace-only → None
    - Valid string → stripped string
    """

    def test_none_returns_none(self):
        """None input should return None."""
        assert _optional_string(None) is None

    def test_empty_string_returns_none(self):
        """Empty string should return None."""
        assert _optional_string("") is None

    def test_whitespace_only_returns_none(self):
        """Whitespace-only string should return None."""
        assert _optional_string("   ") is None

    def test_valid_string_returns_stripped(self):
        """Valid string should be stripped and returned."""
        assert _optional_string("  hello  ") == "hello"


# ─── _require_string ────────────────────────────────────────────────

class TestRequireString:
    """Tests for the _require_string helper.

    This is like _optional_string, but raises an error if the value
    is missing. Used for required fields like user_id and text.
    """

    def test_valid_string_returns_it(self):
        """A valid string should be returned as-is (stripped)."""
        assert _require_string("hello", "msg") == "hello"

    def test_none_raises_error(self):
        """None should raise GenerationValidationError."""
        with pytest.raises(GenerationValidationError, match="required"):
            _require_string(None, "This field is required")

    def test_empty_raises_error(self):
        """Empty string should raise GenerationValidationError."""
        with pytest.raises(GenerationValidationError):
            _require_string("", "This field is required")


# ─── _resolve_voice ─────────────────────────────────────────────────

class TestResolveVoice:
    """Tests for voice resolution.

    _resolve_voice takes a voice value and returns a tuple of
    (normalized_name, provider_voice_name).

    It checks both the VOICE_CATALOG (friendly names like "sigma_male")
    and SUPPORTED_PROVIDER_VOICES (raw OpenAI voices like "ash").
    """

    def test_catalog_voice_resolves(self):
        """A catalog voice like 'sigma_male' should resolve to its provider voice."""
        result = _resolve_voice("sigma_male")
        assert result == ("sigma_male", "ash")

    def test_catalog_voice_with_spaces(self):
        """'Sigma Male' (with space) should normalize and resolve."""
        result = _resolve_voice("Sigma Male")
        assert result == ("sigma_male", "ash")

    def test_provider_voice_resolves(self):
        """A raw provider voice like 'ash' should resolve to itself."""
        result = _resolve_voice("ash")
        assert result == ("ash", "ash")

    def test_unsupported_voice_raises_error(self):
        """An unsupported voice should raise GenerationValidationError."""
        with pytest.raises(GenerationValidationError, match="not supported"):
            _resolve_voice("nonexistent_voice")

    def test_none_voice_raises_error(self):
        """None should raise GenerationValidationError."""
        with pytest.raises(GenerationValidationError, match="required"):
            _resolve_voice(None)


# ─── _resolve_instructions ──────────────────────────────────────────

class TestResolveInstructions:
    """Tests for instruction resolution.

    _resolve_instructions takes a style and fine_tune value and returns
    a tuple of (instruction_text, source).

    Priority: fine_tune > style > default
    """

    def test_fine_tune_overrides_style(self):
        """Fine-tune should win over style."""
        result = _resolve_instructions("horror", "Speak like a pirate")
        assert result == ("Speak like a pirate", "fine_tune")

    def test_style_resolves_to_prompt(self):
        """A valid style should resolve to its predefined prompt."""
        result = _resolve_instructions("horror", None)
        assert "dark, suspenseful" in result[0]
        assert result[1] == "style"

    def test_style_with_spaces_normalizes(self):
        """Style with spaces should normalize correctly."""
        result = _resolve_instructions("  Horror  ", None)
        assert "dark, suspenseful" in result[0]

    def test_invalid_style_raises_error(self):
        """An unsupported style should raise GenerationValidationError."""
        with pytest.raises(GenerationValidationError, match="not supported"):
            _resolve_instructions("nonexistent_style", None)

    def test_no_style_or_fine_tune_returns_default(self, app_context):
        """When neither style nor fine_tune is provided, return the default.

        This test needs app_context because _resolve_instructions accesses
        current_app.config["DEFAULT_TTS_INSTRUCTION"] when no style or
        fine_tune is provided.
        """
        result = _resolve_instructions(None, None)
        assert result[1] == "default"


# ─── _get_week_start_date ───────────────────────────────────────────

class TestGetWeekStartDate:
    """Tests for weekly boundary calculation.

    _get_week_start_date returns the ISO date of the Monday of the
    current week. This is used to track weekly word limits.
    """

    def test_monday_returns_itself(self):
        """If today is Monday, the week start should be today."""
        # A Monday: 2026-05-04
        monday = datetime(2026, 5, 4, tzinfo=timezone.utc)
        assert _get_week_start_date(monday) == "2026-05-04"

    def test_wednesday_returns_monday(self):
        """If today is Wednesday, the week start should be the previous Monday."""
        # A Wednesday: 2026-05-06
        wednesday = datetime(2026, 5, 6, tzinfo=timezone.utc)
        assert _get_week_start_date(wednesday) == "2026-05-04"

    def test_sunday_returns_monday(self):
        """If today is Sunday, the week start should be 6 days ago (Monday)."""
        # A Sunday: 2026-05-10
        sunday = datetime(2026, 5, 10, tzinfo=timezone.utc)
        assert _get_week_start_date(sunday) == "2026-05-04"


# ─── _calculate_days_until_reset ────────────────────────────────────

class TestCalculateDaysUntilReset:
    """Tests for the reset time calculation.

    _calculate_days_until_reset tells the frontend how many days until
    the weekly word limit resets (next Monday).
    """

    def test_monday_returns_7(self):
        """On Monday, reset is 7 days away (next Monday)."""
        monday = datetime(2026, 5, 4, 10, 0, 0, tzinfo=timezone.utc)
        assert _calculate_days_until_reset(monday) == 7

    def test_sunday_returns_1(self):
        """On Sunday, reset is 1 day away (tomorrow is Monday)."""
        sunday = datetime(2026, 5, 10, 10, 0, 0, tzinfo=timezone.utc)
        assert _calculate_days_until_reset(sunday) == 1

    def test_never_returns_negative(self):
        """The result should never be negative (floor at 0)."""
        # Just before midnight on Sunday
        almost_monday = datetime(2026, 5, 10, 23, 59, 59, tzinfo=timezone.utc)
        assert _calculate_days_until_reset(almost_monday) >= 0
