from flask import Blueprint, render_template, request, send_file
from app.utils.tts import text_to_speech
from app.utils.stt import speech_to_text
from app.utils.sentiment import analyze_sentiment
from app.utils.language import detect_language
from langdetect import detect
import os
import time

main = Blueprint('main', __name__)

# Ensure static directories exist
AUDIO_DIR = os.path.join('static', 'audio')
PDF_DIR = os.path.join('static', 'pdfs')
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/tts', methods=['POST'])
def handle_tts():
    text = request.form.get('text')
    
    if not text or text.strip() == '':
        return render_template('index.html', tts_error="❌ Please enter some text")
    
    try:
        timestamp = int(time.time())
        filename = f"tts_output_{timestamp}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)
        
        generated_filepath = text_to_speech(text, filepath)
        if not os.path.exists(generated_filepath):
            return render_template('index.html', tts_error="❌ Failed to generate audio")
        
        return render_template('index.html', tts_path=filename)
    except Exception as e:
        return render_template('index.html', tts_error=f"❌ Error: {str(e)}")

@main.route('/stt', methods=['POST'])
def handle_stt():
    if 'audio' not in request.files:
        return render_template('index.html', stt_error="❌ Please upload an audio file")
    
    file = request.files['audio']
    if file.filename == '':
        return render_template('index.html', stt_error="❌ No file selected")
    
    try:
        result, pdf_path = speech_to_text(file)
        pdf_filename = os.path.basename(pdf_path)
        return render_template('index.html', stt_text=result, pdf_path=pdf_filename)
    except Exception as e:
        return render_template('index.html', stt_error=f"❌ Error: {str(e)}")

@main.route('/sentiment', methods=['POST'])
def handle_sentiment():
    text = request.form.get('text')
    
    if not text or text.strip() == '':
        return render_template('index.html', sentiment_error="❌ Please enter some text")
    
    try:
        sentiment = analyze_sentiment(text)
        return render_template('index.html', sentiment=sentiment)
    except Exception as e:
        return render_template('index.html', sentiment_error=f"❌ Error: {str(e)}")

@main.route('/language', methods=['POST'])
def handle_language():
    text = request.form.get('text')
    
    if not text or text.strip() == '':
        return render_template('index.html', language_error="❌ Please enter some text")

    try:
        code = detect(text)
        language = LANGUAGE_NAMES.get(code, f"Unknown ({code})")
    except Exception as e:
        language = f"❌ Error: {str(e)}"

    return render_template('index.html', language=language)

# Language names dictionary (unchanged)
LANGUAGE_NAMES = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "es": "Spanish",
    "et": "Estonian",
    "fa": "Persian",
    "fi": "Finnish",
    "fr": "French",
    "gu": "Gujarati",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "id": "Indonesian",
    "it": "Italian",
    "ja": "Japanese",
    "kn": "Kannada",
    "ko": "Korean",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mr": "Marathi",
    "ne": "Nepali",
    "nl": "Dutch",
    "no": "Norwegian",
    "pa": "Punjabi",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "sq": "Albanian",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Tagalog",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh-cn": "Chinese (Simplified)",
    "zh-tw": "Chinese (Traditional)"
}