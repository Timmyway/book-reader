import os
import pytest
from dotenv import load_dotenv
from app.services.text_to_speech import TextToSpeech

# Load environment variables from .env file
load_dotenv()

# Get values from the environment
PIPER_PATH = os.getenv("PIPER_PATH", "C:\\piper")  # Fallback if missing
MODELS_DIR = os.getenv("MODELS_DIR", "C:\\piper\\models")  # Fallback if missing

# Get the absolute root folder (where main.py is located)
ROOT_FOLDER = os.getenv("ROOT_FOLDER", os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture
def tts():
    """Fixture to create a fresh instance of TextToSpeech before each test."""
    return TextToSpeech(PIPER_PATH, MODELS_DIR, ROOT_FOLDER)

def test_get_safe_filename(tts):
    """Test safe filename generation."""
    text = "Hello, world!"
    filename = tts.get_safe_filename(text)
    
    assert filename.startswith("static/audio/hello-world-")
    assert filename.endswith(".wav")

def test_get_languages(tts, mocker):
    """Test that languages are correctly listed from the models directory."""
    mocker.patch("os.listdir", return_value=["en", "fr"])
    mocker.patch("os.path.isdir", return_value=True)

    languages = tts.get_languages()
    assert "en" in languages
    assert "fr" in languages

def test_get_models_for_language(tts, mocker):
    """Test retrieving models for a given language."""
    mocker.patch("os.listdir", return_value=["model1.onnx", "model2.onnx"])

    models = tts.get_models_for_language("en")
        
    assert "model1.onnx" in models
    assert "model2.onnx" in models

def test_process_speech_request(tts, mocker):
    """Test that process_speech_request calls generate_speech with correct parameters."""
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch.object(tts, "generate_speech")

    text = "Hello, test"
    selected_language = "en"
    selected_model = "model.onnx"
    output_file = tts.process_speech_request(text, selected_language, selected_model)

    tts.generate_speech.assert_called_once_with(text, os.path.join(MODELS_DIR, selected_language, selected_model), output_file, 1.0)
