from flask import Flask, jsonify
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Blueprints
    from modules.tts.routes import tts_bp

    app.register_blueprint(tts_bp, url_prefix="/tts")


    # Root endpoint
    @app.route("/")
    def home():
        return jsonify({"message": "Weyoto Voice MVP is live"})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=Config.DEBUG)



