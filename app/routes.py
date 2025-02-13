from flask import render_template, request, send_from_directory, jsonify, current_app
import os

def index():
    if request.method == "POST":
        # Get text and language/model choice from the form
        text = request.form["text"]
        selected_language = request.form["language"]
        selected_model = request.form["model"]

        # Retrieve TextToSpeech instance from Flask app context
        text_to_speech = current_app.config['TEXT_TO_SPEECH']

        try:
            # Process the speech request
            output_file = text_to_speech.process_speech_request(text, selected_language, selected_model)
            
            # Show loading message
            status = "Generating speech..."
            
            return render_template("index.html", languages=text_to_speech.get_languages(), models=text_to_speech.get_models_for_language(selected_language), status=status, audio_file=output_file)

        except FileNotFoundError as e:
            # Handle case where model is not found
            return str(e), 404
        except Exception as e:
            # Handle other exceptions
            return f"An error occurred: {str(e)}", 500

    # Retrieve TextToSpeech instance from Flask app context
    text_to_speech = current_app.config['TEXT_TO_SPEECH']
    
    return render_template("index.html", languages=text_to_speech.get_languages(), models=None, status=None)

def models_for_language(language):
    """Fetch models for a selected language via AJAX."""
    text_to_speech = current_app.config['TEXT_TO_SPEECH']
    models = text_to_speech.get_models_for_language(language)
    return jsonify({"models": models})

def serve_audio(filename):
    """Serve the audio file."""
    return send_from_directory('static/audio', filename)
