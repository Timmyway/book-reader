from flask import Flask
from app.routes import index, models_for_language, serve_audio
from app.services.text_to_speech import TextToSpeech

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)

    # Define the paths for Piper and models
    PIPER_PATH = r'G:\Peper\piper\piper.exe'  # Correct path for your Piper executable
    MODELS_DIR = r'G:\Peper\piper\models'     # Correct models directory path

    # Initialize the TextToSpeech service with the necessary paths
    text_to_speech = TextToSpeech(piper_path=PIPER_PATH, models_dir=MODELS_DIR)

    # Make TextToSpeech globally accessible via Flask's app context
    app.config['TEXT_TO_SPEECH'] = text_to_speech

    # Register the routes with the app
    app.add_url_rule('/', view_func=index)
    app.add_url_rule('/models/<language>', view_func=models_for_language)
    app.add_url_rule('/static/audio/<filename>', view_func=serve_audio)

    return app
