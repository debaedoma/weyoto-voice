"""
conftest.py — Shared test configuration.

This file is automatically picked up by pytest. It provides "fixtures"
(reusable test objects) that any test file can use by simply naming them
as a parameter.

What's a fixture?
-----------------
A fixture is a function that sets up something your test needs, then
cleans it up when the test is done. Think of it like a "preparation
assistant" that hands you a ready-to-use object.

Fixtures defined here:
  - app: Creates a fresh Flask app configured for testing
  - client: Creates a Flask test client (makes fake HTTP requests)
  - app_context: Provides a Flask app context for tests that need it
"""

import os
import shutil
import sqlite3
import tempfile
import pytest
from app import create_app


@pytest.fixture
def app():
    """
    Creates a Flask app configured for testing.

    What's happening:
    1. We call create_app() — the same factory function from app.py
    2. We override settings:
       - DATABASE_PATH = temp file — Uses a temporary SQLite database file.
         Unlike ":memory:", a file-based database persists across multiple
         connections (which is how store.py works — it opens a new connection
         each time get_connection() is called).
       - AUDIO_STORAGE_DIR = temp directory — So we don't clutter the
         real instance/audio folder with test files.
       - TESTING = True — Flask gives better error messages.
    3. We create the database tables inside the app context.

    The "yield" instead of "return" means this is a "generator fixture".
    Code before "yield" runs before the test. Code after "yield" runs
    after the test (cleanup).
    """
    # Create a temp directory for audio files
    audio_dir = tempfile.mkdtemp()

    # Create a temp file for the database
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)  # Close the file descriptor immediately

    app = create_app()
    app.config.update({
        "TESTING": True,
        # Use a temp file for the database (not :memory: because store.py
        # opens a new connection each time, and each :memory: connection
        # creates a separate database)
        "DATABASE_PATH": db_path,
        # Use a temp directory for audio so we don't clutter the real one
        "AUDIO_STORAGE_DIR": audio_dir,
        # Disable OpenAI calls during tests (we'll mock them)
        "OPENAI_API_KEY": "test-key-not-real",
    })

    # Create the database tables inside the test app context
    with app.app_context():
        from modules.tts.store import initialize_database
        initialize_database()

    yield app  # This is where the test runs

    # Cleanup: close all SQLite connections and delete the temp files
    # We need to force-close any lingering connections so Windows
    # doesn't complain about file locks.
    try:
        os.unlink(db_path)
    except PermissionError:
        pass  # If still locked, it'll be cleaned up eventually

    shutil.rmtree(audio_dir, ignore_errors=True)


@pytest.fixture
def client(app):
    """
    Creates a Flask test client.

    The test client lets you make fake HTTP requests to your app
    WITHOUT actually starting a server. It's fast and doesn't need
    a port or network connection.

    Usage in tests:
        response = client.get("/voices")
        response = client.post("/generate-voice", json={...})

    The "with" statement ensures proper setup/cleanup of the client.
    """
    with app.test_client() as client:
        yield client


@pytest.fixture
def app_context(app):
    """
    Provides a Flask application context.

    Some functions (like _resolve_instructions when returning the
    default instruction) need to access current_app.config. This
    fixture gives them that access.

    Usage:
        def test_something(app_context):
            # current_app.config is now available
            result = _resolve_instructions(None, None)
    """
    with app.app_context():
        yield
