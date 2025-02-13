import os
from flask import Flask
from app.routes import index, models_for_language, serve_audio, generate_speech
from app.services.text_to_speech import TextToSpeech
from dotenv import load_dotenv

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    # Get values from .env
    piper_path = os.getenv('PIPER_PATH')
    models_dir = os.getenv('MODELS_DIR')

    # Initialize the TextToSpeech service with the necessary paths
    text_to_speech = TextToSpeech(piper_path=piper_path, models_dir=models_dir)

    # Make TextToSpeech globally accessible via Flask's app context
    app.config['TEXT_TO_SPEECH'] = text_to_speech

    # Register the routes with the app
    app.add_url_rule('/', view_func=index)
    app.add_url_rule('/models/<language>', view_func=models_for_language)
    app.add_url_rule('/static/audio/<filename>', view_func=serve_audio)
    app.add_url_rule('/generate', view_func=generate_speech, methods=["POST"])

    return app
