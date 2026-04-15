import sqlite3
from pathlib import Path

from flask import current_app


def get_connection():
    db_path = Path(current_app.config["DATABASE_PATH"])
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    with get_connection() as connection:
        # Keep the schema small for MVP: one table for quota state and one for outputs.
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT,
                words_used_this_week INTEGER NOT NULL DEFAULT 0,
                week_start_date TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS generations (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                text TEXT NOT NULL,
                requested_voice TEXT NOT NULL,
                provider_voice TEXT NOT NULL,
                style TEXT,
                fine_tune TEXT,
                instructions_used TEXT NOT NULL,
                word_count INTEGER NOT NULL,
                audio_url TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE INDEX IF NOT EXISTS idx_generations_user_created_at
            ON generations(user_id, created_at);
            """
        )


def fetch_user(connection, user_id):
    row = connection.execute(
        """
        SELECT id, email, words_used_this_week, week_start_date, created_at, is_active
        FROM users
        WHERE id = ?
        """,
        (user_id,),
    ).fetchone()
    return dict(row) if row else None


def create_user(connection, user_id, email, week_start_date, created_at):
    connection.execute(
        """
        INSERT INTO users (id, email, words_used_this_week, week_start_date, created_at, is_active)
        VALUES (?, ?, 0, ?, ?, 1)
        """,
        (user_id, email, week_start_date, created_at),
    )
    return fetch_user(connection, user_id)


def update_user_email(connection, user_id, email):
    connection.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (email, user_id),
    )


def reset_user_weekly_usage(connection, user_id, week_start_date):
    connection.execute(
        """
        UPDATE users
        SET words_used_this_week = 0, week_start_date = ?
        WHERE id = ?
        """,
        (week_start_date, user_id),
    )


def increment_user_usage(connection, user_id, word_count):
    connection.execute(
        """
        UPDATE users
        SET words_used_this_week = words_used_this_week + ?
        WHERE id = ?
        """,
        (word_count, user_id),
    )


def record_generation(
    connection,
    generation_id,
    user_id,
    text,
    requested_voice,
    provider_voice,
    style,
    fine_tune,
    instructions_used,
    word_count,
    audio_url,
    created_at,
):
    connection.execute(
        """
        INSERT INTO generations (
            id,
            user_id,
            text,
            requested_voice,
            provider_voice,
            style,
            fine_tune,
            instructions_used,
            word_count,
            audio_url,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            generation_id,
            user_id,
            text,
            requested_voice,
            provider_voice,
            style,
            fine_tune,
            instructions_used,
            word_count,
            audio_url,
            created_at,
        ),
    )
