"""
test_routes.py — Integration tests for the API endpoints.

These tests use the Flask test client (from conftest.py) to make
fake HTTP requests to your routes. No server is started — the
requests are handled internally by Flask.

What we're testing:
  - GET  /          — Health check
  - GET  /voices    — List available voices
  - POST /generate-voice — TTS generation (validation, limits)
  - GET  /audio/<filename> — Audio file serving

How the test client works:
    client.get("/voices") sends a fake GET request to /voices.
    The response object has .status_code, .json, .data, etc.
"""

import json
from unittest.mock import patch, MagicMock

import pytest


# ─── GET / ──────────────────────────────────────────────────────────

class TestHealthCheck:
    """Tests for the root health check endpoint."""

    def test_returns_200_and_message(self, client):
        """GET / should return a 200 with a welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json["message"] == "Weyoto Voice MVP is live"


# ─── GET /voices ────────────────────────────────────────────────────

class TestListVoices:
    """Tests for the /voices endpoint."""

    def test_returns_200_and_voices(self, client):
        """GET /voices should return a list of available voices."""
        response = client.get("/voices")
        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert "voices" in response.json

    def test_includes_expected_voices(self, client):
        """The response should include the voices defined in VOICE_CATALOG."""
        response = client.get("/voices")
        voices = response.json["voices"]
        # Check that our catalog voices are present
        assert "sigma_male" in voices
        assert "shes_her" in voices
        assert "lara_croft" in voices
        assert "british_prince" in voices

    def test_voice_has_expected_structure(self, client):
        """Each voice should have label, provider_voice, and preview_url fields."""
        response = client.get("/voices")
        sigma = response.json["voices"]["sigma_male"]
        assert sigma["label"] == "Sigma Male"
        assert sigma["provider_voice"] == "ash"
        # preview_url may be None if the preview file doesn't exist
        assert "preview_url" in sigma


# ─── POST /generate-voice ───────────────────────────────────────────

class TestGenerateVoice:
    """Tests for the TTS generation endpoint.

    These tests check validation logic. We mock the OpenAI API call
    so no real API requests are made.
    """

    def test_missing_user_id_returns_400(self, client):
        """Request without user_id should return 400."""
        response = client.post("/generate-voice", json={
            "text": "Hello world",
            "voice": "sigma_male",
        })
        assert response.status_code == 400
        assert response.json["status"] == "error"
        assert "user_id" in response.json["message"].lower()

    def test_missing_text_returns_400(self, client):
        """Request without text should return 400."""
        response = client.post("/generate-voice", json={
            "user_id": "test-user",
            "voice": "sigma_male",
        })
        assert response.status_code == 400
        assert response.json["status"] == "error"
        assert "text" in response.json["message"].lower()

    def test_missing_voice_returns_400(self, client):
        """Request without voice should return 400."""
        response = client.post("/generate-voice", json={
            "user_id": "test-user",
            "text": "Hello world",
        })
        assert response.status_code == 400
        assert response.json["status"] == "error"

    def test_unsupported_voice_returns_400(self, client):
        """Request with an unsupported voice should return 400."""
        response = client.post("/generate-voice", json={
            "user_id": "test-user",
            "text": "Hello world",
            "voice": "nonexistent_voice",
        })
        assert response.status_code == 400
        assert "not supported" in response.json["message"]

    def test_text_too_long_returns_400(self, client):
        """Request with text exceeding MAX_WORDS_PER_GENERATION should return 400."""
        # Generate text with more than 120 words (the default limit)
        long_text = "word " * 121
        response = client.post("/generate-voice", json={
            "user_id": "test-user",
            "text": long_text,
            "voice": "sigma_male",
        })
        assert response.status_code == 400
        assert "exceeds" in response.json["message"].lower()

    def test_fine_tune_too_long_returns_400(self, client):
        """Request with fine_tune exceeding MAX_FINE_TUNE_WORDS should return 400."""
        long_fine_tune = "word " * 26  # Default max is 25
        response = client.post("/generate-voice", json={
            "user_id": "test-user",
            "text": "Hello world",
            "voice": "sigma_male",
            "fine_tune": long_fine_tune,
        })
        assert response.status_code == 400
        assert "fine-tune" in response.json["message"].lower()

    def test_successful_generation_returns_201(self, client):
        """
        A valid request should return 201 with generation details.

        We mock the OpenAI API call so no real request is made.
        """
        # Mock the OpenAI client's streaming response
        mock_response = MagicMock()
        mock_response.stream_to_file = MagicMock()

        with patch("modules.tts.logic.client.audio.speech.with_streaming_response.create") as mock_create:
            mock_create.return_value.__enter__.return_value = mock_response

            response = client.post("/generate-voice", json={
                "user_id": "test-user",
                "text": "Hello world, this is a test.",
                "voice": "sigma_male",
            })

        assert response.status_code == 201
        assert response.json["status"] == "success"
        assert "generation_id" in response.json
        assert "audio_url" in response.json
        assert response.json["audio_url"].startswith("/audio/")
        assert response.json["words_used"] == 6  # "Hello world, this is a test." = 6 words
        assert "words_remaining" in response.json
        assert response.json["voice"] == "sigma_male"

    def test_generation_with_style(self, client):
        """A request with a style should succeed."""
        mock_response = MagicMock()
        mock_response.stream_to_file = MagicMock()

        with patch("modules.tts.logic.client.audio.speech.with_streaming_response.create") as mock_create:
            mock_create.return_value.__enter__.return_value = mock_response

            response = client.post("/generate-voice", json={
                "user_id": "test-user",
                "text": "Hello world",
                "voice": "sigma_male",
                "style": "horror",
            })

        assert response.status_code == 201
        assert response.json["instruction_source"] == "style"

    def test_generation_with_fine_tune(self, client):
        """A request with a fine_tune instruction should succeed and override style."""
        mock_response = MagicMock()
        mock_response.stream_to_file = MagicMock()

        with patch("modules.tts.logic.client.audio.speech.with_streaming_response.create") as mock_create:
            mock_create.return_value.__enter__.return_value = mock_response

            response = client.post("/generate-voice", json={
                "user_id": "test-user",
                "text": "Hello world",
                "voice": "sigma_male",
                "style": "horror",
                "fine_tune": "Speak like a calm narrator",
            })

        assert response.status_code == 201
        assert response.json["instruction_source"] == "fine_tune"

    def test_weekly_limit_tracking(self, client):
        """
        The weekly word limit should decrease after each generation.

        We generate twice and check that words_remaining decreases.
        """
        mock_response = MagicMock()
        mock_response.stream_to_file = MagicMock()

        with patch("modules.tts.logic.client.audio.speech.with_streaming_response.create") as mock_create:
            mock_create.return_value.__enter__.return_value = mock_response

            # First generation: 6 words
            resp1 = client.post("/generate-voice", json={
                "user_id": "limit-test-user",
                "text": "Hello world, this is a test.",
                "voice": "sigma_male",
            })
            assert resp1.status_code == 201
            remaining_after_first = resp1.json["words_remaining"]

            # Second generation: 3 words
            resp2 = client.post("/generate-voice", json={
                "user_id": "limit-test-user",
                "text": "More words here",
                "voice": "sigma_male",
            })
            assert resp2.status_code == 201
            remaining_after_second = resp2.json["words_remaining"]

            # After the second generation, we should have 3 fewer words remaining
            # (6 from first + 3 from second = 9 words used)
            assert remaining_after_second == remaining_after_first - 3

    def test_weekly_limit_exceeded_returns_429(self, client):
        """
        When the weekly word limit is reached, the API should return 429.

        We set WEEKLY_WORD_LIMIT to a small value and generate until we
        exceed it.
        """
        mock_response = MagicMock()
        mock_response.stream_to_file = MagicMock()

        # Override the weekly limit to a small value for this test
        from flask import current_app

        with patch("modules.tts.logic.client.audio.speech.with_streaming_response.create") as mock_create:
            mock_create.return_value.__enter__.return_value = mock_response

            # Use the app context to modify config
            with client.application.app_context():
                original_limit = current_app.config["WEEKLY_WORD_LIMIT"]
                current_app.config["WEEKLY_WORD_LIMIT"] = 5  # Only 5 words per week!

            # First request: 3 words — should succeed
            resp1 = client.post("/generate-voice", json={
                "user_id": "limit-exceed-user",
                "text": "one two three",
                "voice": "sigma_male",
            })
            assert resp1.status_code == 201

            # Second request: 3 more words — should exceed the 5-word limit
            resp2 = client.post("/generate-voice", json={
                "user_id": "limit-exceed-user",
                "text": "four five six",
                "voice": "sigma_male",
            })
            assert resp2.status_code == 429
            assert resp2.json["status"] == "limit_reached"
            assert "reset_in_days" in resp2.json

            # Restore the original limit
            with client.application.app_context():
                current_app.config["WEEKLY_WORD_LIMIT"] = original_limit

    def test_all_three_route_aliases_work(self, client):
        """
        The three route decorators should all point to the same handler.

        POST /generate, POST /generate-voice, and POST /tts/generate-voice
        should all work identically.
        """
        mock_response = MagicMock()
        mock_response.stream_to_file = MagicMock()

        with patch("modules.tts.logic.client.audio.speech.with_streaming_response.create") as mock_create:
            mock_create.return_value.__enter__.return_value = mock_response

            payload = {
                "user_id": "alias-test",
                "text": "Test",
                "voice": "sigma_male",
            }

            # Test all three routes
            resp1 = client.post("/generate", json=payload)
            resp2 = client.post("/generate-voice", json=payload)
            resp3 = client.post("/tts/generate-voice", json=payload)

            assert resp1.status_code == 201
            assert resp2.status_code == 201
            assert resp3.status_code == 201


# ─── GET /audio/<filename> ──────────────────────────────────────────

class TestGetAudio:
    """Tests for the audio file serving endpoint."""

    def test_nonexistent_audio_returns_404(self, client):
        """Requesting a non-existent audio file should return 404."""
        response = client.get("/audio/nonexistent.mp3")
        assert response.status_code == 404

    def test_audio_serving_returns_mp3(self, client, app):
        """
        An existing audio file should be served with the correct MIME type.

        We create a temporary audio file and request it. The temp directory
        is cleaned up automatically by the app fixture (shutil.rmtree), so
        we don't need to manually delete the file here.
        """
        import os

        # Create a temporary audio file in the app's audio directory
        audio_dir = app.config["AUDIO_STORAGE_DIR"]
        os.makedirs(audio_dir, exist_ok=True)

        test_filename = "test_audio.mp3"
        test_filepath = os.path.join(audio_dir, test_filename)

        # Write some dummy MP3 content
        with open(test_filepath, "wb") as f:
            f.write(b"fake mp3 content")

        response = client.get(f"/audio/{test_filename}")
        assert response.status_code == 200
        assert response.mimetype == "audio/mpeg"
        assert response.data == b"fake mp3 content"
