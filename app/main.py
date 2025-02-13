import os
from flask import Flask
from app.routes import index, models_for_language, serve_audio, generate_speech, check_task_status, get_languages, list_audio_files, serve_audio
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
    text_to_speech = TextToSpeech(piper_path=piper_path, models_dir=models_dir, root_folder=app.root_path)

    # Make TextToSpeech globally accessible via Flask's app context
    app.config['TEXT_TO_SPEECH'] = text_to_speech

   # Register the routes
    app.add_url_rule('/', view_func=index)  # Home page or the main form
    app.add_url_rule('/models/<language>', view_func=models_for_language)  # Models for a specific language
    app.add_url_rule('/static/audio/<filename>', view_func=serve_audio)  # Serving the generated audio file
    app.add_url_rule('/generate', view_func=generate_speech, methods=["POST"])  # Route to generate speech
    app.add_url_rule('/check_status/<task_id>', view_func=check_task_status)  # Route to check the task's status
    app.add_url_rule('/languages', view_func=get_languages)  # Route to get available languages

    # Add the routes for listing and serving audio files
    app.add_url_rule('/audio_files', view_func=list_audio_files)  # Route to list all audio files
    app.add_url_rule('/static/audio/<filename>', view_func=serve_audio)  # Route to serve audio file

    return app
