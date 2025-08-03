from openai import OpenAI
from pathlib import Path
import uuid
import os

client = OpenAI()  # Reads OPENAI_API_KEY from env

def generate_voice_stream(text, voice, instructions):
    filename = f"{uuid.uuid4()}.mp3"
    output_dir = Path("app/static/audio") / filename
    output_dir.mkdir(parents=True, exist_ok=True)  # ✅ Ensure folder exists

    output_path = output_dir / filename

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        input=text,
        voice=voice,
        instructions=instructions
    ) as response:
        response.stream_to_file(output_path)

    return output_path
