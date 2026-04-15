from flask import Blueprint, current_app, jsonify, render_template, request, send_from_directory

from .logic import (
    GenerationValidationError,
    WeeklyLimitReachedError,
    list_available_voices,
    process_generation_request,
)

tts_bp = Blueprint("tts", __name__, template_folder="templates")


@tts_bp.route("/tts")
def tts_ui():
    return render_template("index.html")


@tts_bp.route("/generate", methods=["POST"])
@tts_bp.route("/generate-voice", methods=["POST"])
@tts_bp.route("/tts/generate-voice", methods=["POST"])
def generate_voice():
    data = request.get_json(silent=True) or {}

    try:
        response_payload = process_generation_request(data)
        return jsonify(response_payload), 201
    except GenerationValidationError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 400
    except WeeklyLimitReachedError as exc:
        return (
            jsonify(
                {
                    "status": "limit_reached",
                    "message": str(exc),
                    "reset_in_days": exc.reset_in_days,
                }
            ),
            429,
        )
    except Exception:
        current_app.logger.exception("Voice generation failed")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Unable to generate voice right now",
                }
            ),
            500,
        )


@tts_bp.route("/voices", methods=["GET"])
def voices():
    return jsonify({"status": "success", "voices": list_available_voices()})


@tts_bp.route("/audio/<path:filename>", methods=["GET"])
def get_audio(filename):
    # Audio files stay on local disk for MVP, so this route simply serves them back.
    return send_from_directory(
        current_app.config["AUDIO_STORAGE_DIR"],
        filename,
        mimetype="audio/mpeg",
        as_attachment=False,
    )
