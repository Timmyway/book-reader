from flask import render_template, request, send_from_directory, jsonify, current_app
import os

def index():
    """Render the main page with available languages."""
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

def generate_speech():
    if request.method == "POST":
        text = request.form.get("text")
        selected_language = request.form.get("language")
        selected_model = request.form.get("model")

        text_to_speech = current_app.config['TEXT_TO_SPEECH']

        try:
            # Process the speech request
            output_file = text_to_speech.process_speech_request(text, selected_language, selected_model)
            
            # Show loading message
            status = "Generating speech..."
            
            return render_template("index.html", 
                                   languages=text_to_speech.get_languages(), 
                                   models=text_to_speech.get_models_for_language(selected_language), 
                                   status=status, 
                                   audio_file=output_file)

        except FileNotFoundError as e:
            return str(e), 404
        except Exception as e:
            return f"An error occurred: {str(e)}", 500