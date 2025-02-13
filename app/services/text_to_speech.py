import os
import subprocess
import re
import unicodedata

class TextToSpeech:
    def __init__(self, piper_path, models_dir):
        """Initialize the TextToSpeech object with Piper executable path and models directory."""
        self.piper_path = piper_path
        self.models_dir = models_dir

    def get_languages(self):
        """Dynamically load languages from the models directory."""
        return [lang for lang in os.listdir(self.models_dir) if os.path.isdir(os.path.join(self.models_dir, lang))]

    def get_models_for_language(self, language):
        """Get all models for a given language."""
        language_path = os.path.join(self.models_dir, language)
        return [f for f in os.listdir(language_path) if f.endswith('.onnx')]

    def get_safe_filename(self, text):
        """Generate a safe, slugified filename based on the input text."""
        # Normalize the text to remove accents
        normalized_text = unicodedata.normalize('NFKD', text[:50]).encode('ascii', 'ignore').decode('ascii')
        
        # Replace non-alphanumeric characters (except spaces) with an empty string
        slugified_text = re.sub(r'[^a-zA-Z0-9\s]', '', normalized_text)
        
        # Replace spaces with hyphens and convert to lowercase
        safe_text = re.sub(r'\s+', '-', slugified_text).lower()
        
        return f"static/audio/{safe_text}.wav"

    def generate_speech(self, text, model_path, output_file):
        """Run the Piper executable to generate speech from text."""

        # Define the correct command for Piper
        command = f'"{self.piper_path}" --model "{model_path}" --output_file "{output_file}"'
        
        try:
            # Run Piper with the given command
            process = subprocess.run(command, shell=True, text=True, input=text, capture_output=True)

            # Debugging: Print Piper output
            print("== Piper Output =>", process.stdout)
            print("== Piper Error =>", process.stderr)

            if process.returncode != 0:
                raise Exception(f"Error running Piper: {process.stderr}")

        except Exception as e:
            print(f"Error in generate_speech: {e}")
            raise

    def process_speech_request(self, text, selected_language, selected_model):
        """Process the text-to-speech request and return the output file path."""        
        model_path = os.path.join(self.models_dir, selected_language, selected_model)
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        output_file = self.get_safe_filename(text)
        print('== Output file =>', output_file)
        print('== Model path =>', model_path)
        print('== Text =>', text)
        self.generate_speech(text, model_path, output_file)
        
        return output_file

