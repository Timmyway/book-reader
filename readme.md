# **Book Reader - AI-Powered Text-to-Speech**  

🚀 **Book Reader** is an AI-powered text-to-speech (TTS) application that converts text into high-quality speech using various models. It supports multiple languages and formats, allowing users to generate and listen to audio files easily.  

## 🌟 **Features**  
- 🎙️ Generate speech from text using AI models  
- 🌍 Supports multiple languages  
- 📂 Outputs in WAV formats  
- ⚡ Asynchronous background processing  
- 🎵 List and play generated audio files  

## 🛠 **Tech Stack**  
- **Frontend:** Alpine.js, Bootstrap  
- **Backend:** Flask (Python)  
- **Database:** SQLite / MySQL (for task management)  
- **TTS Models:** ONNX-based models  

## 📦 **Installation**  

1️⃣ **Clone the repository:**  
```sh
git clone https://github.com/your-username/book-reader.git  
cd book-reader
```

2️⃣ Set up a virtual environment (optional but recommended):
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

3️⃣ Install dependencies:
```sh
pip install -r requirements.txt
```

4️⃣ Run the application:
```sh
flask run
```

The app will be available at http://127.0.0.1:5000/ 🎉

📌 Usage
Enter your text in the input field.
Select a language and a speech model.
Click Generate Speech and wait for processing.
Listen or download the generated audio from the listed files.

🚀 API Endpoints
GET /languages → Fetch available languages
GET /models/<language> → Get models for a language
POST /generate → Generate speech (returns task ID)
GET /check_status/<task_id> → Check generation status
GET /audio_files → List generated audio files

🤝 Contributing
Pull requests are welcome! Feel free to open an issue for discussions.