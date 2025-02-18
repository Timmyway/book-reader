from flask import render_template, request, send_from_directory, jsonify, current_app
import os, json, threading, uuid

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

def background_generate_speech(text_to_speech, task_id, text, selected_language, selected_model, rate, name):
    """Run speech generation in the background and update status."""
    
    # Manually push the app and request context for the background thread    
    save_task_status(task_id, "processing")    
    try:
        # Process the speech request and save output file path
        output_file = text_to_speech.process_speech_request(text, selected_language, selected_model, rate, name)
        save_task_status(task_id, "completed")
    except Exception as e:
        save_task_status(task_id, f"failed: {str(e)}")
        return str(e)

    return output_file

def save_task_status(task_id, status):
    """Save task status to a JSON file (or use a database)."""
    status_file = "task_status.json"
    
    if os.path.exists(status_file):
        with open(status_file, "r") as f:
            tasks = json.load(f)
    else:
        tasks = {}

    tasks[task_id] = status

    with open(status_file, "w") as f:
        json.dump(tasks, f)

def generate_speech():
    if request.method == "POST":
        text = request.form.get("text")
        selected_language = request.form.get("language")
        selected_model = request.form.get("model")  
        rate = float(request.form.get("rate", 1.0))  # Default rate is 1.0 if not provided      
        name = request.form.get('name', None)

        task_id = str(uuid.uuid4())  # Generate a unique task ID
        with current_app.app_context():  # Pushing app context
            text_to_speech = current_app.config['TEXT_TO_SPEECH']
            thread = threading.Thread(target=background_generate_speech, args=(text_to_speech, task_id, text, selected_language, selected_model, rate, name))
        thread.start()

        return jsonify({"task_id": task_id, "status": "Processing in the background..."})
    
def check_task_status(task_id):
    """Check the status of a task."""
    status_file = "task_status.json"
    
    if os.path.exists(status_file):
        with open(status_file, "r") as f:
            tasks = json.load(f)
        return jsonify({"status": tasks.get(task_id, "unknown")})
    
    return jsonify({"status": "unknown"})

def get_languages():
    """Return available languages for speech generation."""
    languages = ['fr', 'gb', 'us', 'es']  # Example list
    return jsonify({"languages": languages})

def list_audio_files(order_by = 'desc'):
    """List all generated audio files in the 'static/audio' directory."""
    audio_dir = os.path.join(current_app.root_path, 'static', 'audio')
    
    try:
        # List all files in the audio directory
        audio_files = [
            file for file in os.listdir(audio_dir)
            if file.endswith(('.mp3', '.wav', '.ogg'))
        ]

        # Convert to full paths and filter out missing files
        audio_files_with_ctime = []
        for file in audio_files:
            file_path = os.path.join(audio_dir, file)
            if os.path.exists(file_path):  # Ensure file exists before accessing metadata
                audio_files_with_ctime.append((file, os.path.getmtime(file_path)))

        # Sort by creation time (oldest first)
        reverse = order_by == 'desc'  # True if 'desc', False if 'asc'
        audio_files_with_ctime.sort(key=lambda x: x[1], reverse=reverse)

        # Extract only filenames for response
        sorted_files = [file[0] for file in audio_files_with_ctime]
        
        return jsonify({"audio_files": sorted_files})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def serve_audio(filename):
    """Serve the audio file stored in the 'static/audio' directory."""    
    audio_dir = os.path.join(current_app.root_path, 'static', 'audio')
    try:
        return send_from_directory(audio_dir, filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404