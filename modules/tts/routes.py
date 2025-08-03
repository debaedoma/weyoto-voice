from flask import Blueprint, request, render_template, send_file
from .logic import generate_voice_stream

tts_bp = Blueprint("tts", __name__, template_folder="templates")

@tts_bp.route("/tts")
def tts_ui():
    return render_template("tts.html")

@tts_bp.route("/generate-voice", methods=["POST"])
def generate_voice():
    data = request.json
    text = data.get("text")
    voice = data.get("voice", "coral")
    instructions = data.get("instructions", "Speak naturally.")

    file_path = generate_voice_stream(text, voice, instructions)
    return send_file(file_path, mimetype="audio/mpeg", as_attachment=True)